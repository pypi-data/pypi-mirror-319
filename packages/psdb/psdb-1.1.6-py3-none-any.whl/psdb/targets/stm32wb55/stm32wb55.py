# Copyright (c) 2020 by Phase Advanced Sensor Systems, Inc.
import struct

import psdb
from psdb.devices.stm32wb55.ipc import IPC
from psdb.devices import MemDevice, RAMDevice, stm32, stm32wb55
from psdb.targets import Target
from . import dbgmcu


DEVICES = [(RAMDevice,        'SRAM1',    0x20000000, 0x00030000),
           (RAMDevice,        'SRAM2a',   0x20030000, 0x00008000),
           (RAMDevice,        'SRAM2b',   0x20038000, 0x00008000),
           (stm32.GPT32,      'TIM2',     0x40000000),
           (stm32.USB,        'USB',      0x40006800),
           (stm32.DMA,        'DMA1',     0x40020000),
           (stm32.DMA,        'DMA2',     0x40020400),
           (stm32.DMAMUX,     'DMAMUX',   0x40020800, 14, 4),
           (stm32.GPIO,       'GPIOA',    0x48000000),
           (stm32.GPIO,       'GPIOB',    0x48000400),
           (stm32.GPIO,       'GPIOC',    0x48000800),
           (stm32.GPIO,       'GPIOD',    0x48000C00),
           (stm32.GPIO,       'GPIOE',    0x48001000),
           (stm32.GPIO,       'GPIOH',    0x48001C00),
           (stm32.ADC,        'ADC1',     0x50040000, 1, 1),
           (stm32wb55.RCC,    'RCC',      0x58000000),
           (stm32wb55.PWR,    'PWR',      0x58000400),
           (stm32wb55.IPCC,   'IPCC',     0x58000C00),
           (stm32wb55.FLASH,  'FLASH',    0x58004000, 0x08000000, 3300000,
                                          0x1FFF7000, 1024),  # noqa: E127
           ]


class STM32WB55(Target):
    def __init__(self, db):
        # Max SWD speed is:
        #   55.0 MHz for 2.70V < VDD < 3.6V
        #   35.0 MHz for 1.65V < VDD < 3.6V
        super().__init__(db, 35000000)
        self.ahb_ap     = self.db.aps[0]
        self.uuid       = self.ahb_ap.read_bulk(0x1FFF7590, 12)
        self.flash_size = (self.ahb_ap.read_32(0x1FFF75E0) & 0x0000FFFF)*1024
        self.package    = self.ahb_ap.read_32(0x1FFF7500) & 0x0000001F
        self.mcu_idcode = self.ahb_ap.read_32(0xE0042000)

        self._gen_ble_mac_addr()

        for d in DEVICES:
            cls  = d[0]
            name = d[1]
            addr = d[2]
            args = d[3:]
            cls(self, self.ahb_ap, name, addr, *args)

        self.flash = self.devs['FLASH']
        MemDevice(self, self.ahb_ap, 'FBANKS', self.flash.mem_base,
                  self.flash.user_flash_size)
        MemDevice(self, self.ahb_ap, 'OTP', self.flash.otp_base,
                  self.flash.otp_len)
        self.devs['SRAM2a'].size = self.flash.user_sram2a_size
        self.devs['SRAM2b'].size = self.flash.user_sram2b_size

        ipccdba  = self.flash.get_ipccdba()
        sram1    = self.devs['SRAM1']
        sram2a   = self.devs['SRAM2a']
        size     = sram2a.size - (ipccdba - sram2a.dev_base)
        self.ipc = IPC(self, self.ahb_ap, ipccdba, size, sram1.dev_base)

    def __repr__(self):
        return 'STM32WB55 MCU_IDCODE 0x%08X' % self.mcu_idcode

    def _gen_ble_mac_addr(self):
        '''
        This is the same algorithm that ST uses to generate a Bluetooth address.
        There's some really weird stuff going on here; more research is
        required.  The 24-bit "ST ID" field is 00:80:E1 which is the ST MAC OUI
        and nothing to do with the ST 16-bit Bluetooth company ID (which is
        0x0030).  It looks like this is supposed to generate an EUI-48 address,
        however they are only using 16-bits of their 24-bit OUI and then
        stuffing 8-bits of a "device ID" (0x26 on the STM32WB55xx) into the
        rest of the OUI field and then only using 24-bits of their 32-bit
        unique device number field.

        Essentially, this whole algorithm seems to be crap.  (Or, possibly I
        need to learn more about this stuff).  We'll revisit this in the
        future.
        '''
        self.uid64_raw    = self.ahb_ap.read_bulk(0x1FFF7580, 8)
        self.uid64        = struct.unpack('<Q', self.uid64_raw)[0]
        self.uid64_udn    = ((self.uid64 >>  0) & 0xFFFFFFFF)
        self.uid64_dev_id = ((self.uid64 >> 32) & 0x000000FF)
        self.uid64_st_id  = ((self.uid64 >> 40) & 0x00FFFFFF)
        assert self.uid64_udn != 0xFFFFFFFF
        self.ble_mac_addr = bytes([
            (self.uid64_st_id  >>  8) & 0xFF,
            (self.uid64_st_id  >>  0) & 0xFF,
            (self.uid64_dev_id >>  0) & 0xFF,
            (self.uid64_udn    >> 16) & 0xFF,
            (self.uid64_udn    >>  8) & 0xFF,
            (self.uid64_udn    >>  0) & 0xFF,
            ])

    def configure_rf_clocks(self):
        '''
        Configures all clock subsystems as required for the BLE firmware to be
        able to boot up and start handling commands.
        '''
        rcc = self.devs['RCC']
        pwr = self.devs['PWR']

        # Tune the 32 MHz oscillator.
        rcc.apply_hse_tuning()

        # Enable access to the backup domain.
        pwr.unlock_backup_domain()

        # Reset the backup domain.
        rcc.reset_backup_domain()

        # Enable the LSE drive capability.
        rcc.set_lse_drive_capability(0)

        # Set voltage range 1 (up to 64 MHz).
        pwr.set_voltage_scaling(1)

        # Enable oscillators.
        rcc.enable_hse()
        rcc.enable_hsi()
        rcc.enable_lse()

        # Configure all clock prescalers.
        self.flash.set_wait_states(1)
        rcc.set_hpre(1)
        rcc.set_c2hpre(1)
        rcc.set_shdhpre(1)
        rcc.set_ppre1(1)
        rcc.set_ppre2(1)

        # Select SYSCLOCK = HSE.
        rcc.set_sysclock_source(2)

        # Select other clock sources:
        #   RTCCLOCK      = LSE
        #   USART1CLOCK   = PCLK
        #   LPUARTCLOCK   = PCLK
        #   RFWAKEUPCLOCK = LSE
        #   SMPSCLOCK     = HSE
        #   SMPSDIV       = RANGE1
        rcc.set_rtcclock_source(1)
        rcc.set_usart1clock_source(0)
        rcc.set_lpuartclock_source(0)
        rcc.set_rfwakeupclock_source(1)
        rcc.set_smps_div(1)
        rcc.set_smpsclock_source(2)

    @staticmethod
    def is_mcu(db):
        # APSEL 0 should be populated.
        if set(db.aps) != set((0, 1)):
            return False

        # APSEL 0 and 1 should be AHB3 APs.
        ap = db.aps[0]
        if not isinstance(ap, psdb.access_port.AHB3AP):
            return False
        ap = db.aps[1]
        if not isinstance(ap, psdb.access_port.AHB3AP):
            return False

        # Identify the STM32WB55 through the base component's CIDR/PIDR
        # registers.
        c = db.aps[0].base_component
        if not c:
            c = db.aps[0].probe_components(match=False, recurse=False)
        if not c:
            return False
        if c.cidr != 0xB105100D:
            return False
        if c.pidr != 0xA0495:
            return False

        # Finally, we can match on the DBGMCU IDC value.
        if dbgmcu.read_idc_dev_id(db) != 0x495:
            return False

        return True

    @staticmethod
    def pre_probe(db, verbose):
        # Ensure this is an STM32WB55 part.
        if not STM32WB55.is_mcu(db):
            return

        # Enable all the clocks we want to use.
        cr = dbgmcu.read_cr(db)
        if (cr & 0x00000007) != 0x00000007:
            if verbose:
                print('Detected STM32WB55, enabling all DBGMCU debug clocks.')
            dbgmcu.write_cr(db, cr | 0x00000007)

    @staticmethod
    def probe(db):
        # Ensure this is an STM32WB55 part.
        if not STM32WB55.is_mcu(db):
            return

        # While the STM32WB55 has two CPUs, the second one is inaccessible due
        # to ST security.
        if len(db.cpus) != 1:
            return None

        return STM32WB55(db)
