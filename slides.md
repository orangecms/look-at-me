---
author: Daniel Maslowski
title: Look at ME!
subtitle: Investigating Intel ME Firmware
---

## Disclaimer

### This is not about whether we should trust Intel or any (chip) vendor.

### Many details about the ME are not public or scattered across the web.

### I probably have errors in some places; please report them to me.

## Agenda

- Introduction
- Open Source Firmware
- Intel x86 Hardware
- Motivation
- Firmware Analysis
- Conclusion

# Introduction

## Microcontrollers and fun

:::::::::::::: {.columns}
::: {.column width="2%"}
:::
::: {.column width="32%"}
![Arduino](img/arduino.png){ height=30% }
:::
::: {.column width="2%"}
:::
::: {.column width="32%"}
![ESP8266](img/esp8266.png){ height=30% }
:::
::: {.column width="32%"}
![Network of Things](img/network-of-things.jpg){ height=30% }
:::
::::::::::::::

## Microcontrollers and SoCs on your x86 mainboard

:::::::::::::: {.columns height=30%}
::: {.column width="38%"}
- Chipset (southbridge)
- Gigabit Ethernet (Gbe)
- USB controller
- PCI(e)
- SATA
- GPU
- HD Audio
- Bluetooth module
- Wi-Fi module
- Trusted Platform Module (TPM)
- Embedded Controller (EC)
- Baseboard Management Controller (BMC)
- ...
:::
::: {.column width="62%"}
![Kaby Lake U Mobile block diagram](img/kaby-lake-u-mobile-block-diagram.png){width=100%}

Kaby Lake U Mobile block diagram adapted from [Intel specifications](https://www.intel.com/content/www/us/en/embedded/products/kaby-lake-u/specifications.html)
:::
::::::::::::::

# Open Source Firmware

## Open Source Firmware projects

### Host (CPU, main SoC, chipset)

- coreboot
- LinuxBoot
    * Heads
    * u-root

### Embedded Controller (EC)

- [Chromium OS EC](https://chromium.googlesource.com/chromiumos/platform/ec/+/master/README.md)
- [System76 EC](https://github.com/system76/ec)

### Baseboard Management Controller (BMC)

- OpenBMC
- u-bmc

# Intel x86 Hardware

## Intel chipsets

![Intel Series 300 Chipset](img/intel-chipset-300.png){width=100%}

## A closer look: Denverton platform

### see [Intel website](https://www.intel.com/content/www/us/en/design/products-and-solutions/processors-and-chipsets/denverton/ns/atom-processor-c3000-series.html) and [WikiChip](https://en.wikichip.org/wiki/intel/cores/denverton)

:::::::::::::: {.columns}
::: {.column width="40%"}

![Denverton block diagram](img/denverton-block-diagram.png){ width=100% }

:::
::: {.column width="60%"}

> The platform extends industry-leading performance per watt, low thermal design power (TDP), and unprecedented levels of configurable high-speed I/O for accelerated *innovation* across networking, storage, Internet of Things (IoT), and scalable solutions.

### So what is this...?

- [Management Engine](https://www.intel.com/content/www/us/en/support/articles/000008927/software/chipset-software.html)
- Innovation Engine

:::
::::::::::::::

## Innovation Engine

> Enables next-generation systems to customize solution *firmware* to drive greater operational efficiency, security, and predictive maintenance.

### No use of it is known so far.

## Intel Management Engine (today)

- Microcontroller unit (MCU)
- part of chipset or System on Chip (SoC)
- connected to SPI flash, CPU, GbE
- started from Active Management Technology (AMT)
- may offer runtime services
- can verify host firmware

## Intel platform boot sequence

![](bootseq/bootseq.png){ height=75% }

## AMT, MEI and ISH

### Active Management Technology

- available through MEI driver
    * hardware monitoring
    * power control
    * OS updates
    * storage
    * proxy for KVM (keyboard, video, mouse)

### Management Engine Interface

-  implemented in [Linux kernel](https://www.kernel.org/doc/html/latest/driver-api/mei/index.html)

### Integrated Sensor Hub

- dedicated low power co-processor
- implemented in [Linux Kernel](https://www.kernel.org/doc/Documentation/hid/intel-ish-hid.txt)

## MEBX

### Management Engine BIOS Extensions

- configuration interface in host firmware
- [Ctrl + P](https://wiki.fysik.dtu.dk/it/Intel_AMT#management-engine-bios-extension-mebx) or [F6](hp something TODO)
- default password is `admin`

## Once upon a time...

![ME timeline](timeline/me-timeline.png)

adapted from [Igor Skochinksy - Intel ME Myths and Reality](https://ftp.halifax.rwth-aachen.de/ccc/congress/2017/slides-pdf/34c3-8782-intel_me_myths_and_reality.pdf),

Wikipedia and Intel

## Intel ME Version 12.0

- [release notes are public](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/default.htm?turl=WordDocuments%2Fintelamtrelease120architecture.htm)
- supports TLS 1.2, dropped 1.0
- `CIM_Battery` class
- [AMT can be disabled](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/default.htm?turl=WordDocuments%2Fdisablingintelamt.htm)
- category of "super_critical" events

## ME Firmware Variants

+--------+--------------------------+
| CON(S) | Consumer                 |
+--------+--------------------------+
| COR(P) | Corporate                |
+--------+--------------------------+
| SLM(?) | Slim                     |
+--------+--------------------------+
| SPS    | Server Platform Services |
+--------+--------------------------+
| IGN(?) | Ignition                 |
+--------+--------------------------+

# Motivation

## First public release of a [redistributable ME firmware binary](https://edk2.groups.io/g/devel/message/50920)

### EDK II non-osi mailing list

> Ignition Firmware is a variant of ME firmware that is intended to provide
> lightweight chipset initialization. It does not contain all the features
> of the Intel® Server Platform Services (SPS) ME firmware. Ignition Firmware
> is consequently much smaller than Intel® SPS Firmware (~0.5 MB vs. ~3 MB).

### Build and distribute full firmware images with binaries

- Firmware Support Package (FSP) for host firmware
- Ignition ME firmware for Cascade Lake / Purley

## Follow the yellow brick road...

![Yellow brick road](img/wizard-of-oz_yellow-brick-road.png){ height=80% }

## ME Ignition Firmware License

> Redistribution and use in binary form, without modification, are permitted,
> provided that the following conditions are met:
> 
> 1.  Redistributions must reproduce the above copyright notice and the
>     following disclaimer in the documentation and/or other materials provided
>     with the distribution.
> 
> 2.  Neither the name of Intel Corporation nor the names of its suppliers may
>     be used to endorse or promote products derived from this software without
>     specific prior written permission.
> 
> 3.  No reverse engineering, decompilation, or disassembly of this software
>     is permitted.

## Pay no attention to that man behind the curtain!

![Behind the curtain](img/wizard-of-oz_behind-the-curtain.jpeg){ height=80% }

## Philosophy

[training for FSP by Intel](https://www.intel.com/content/dam/www/public/us/en/documents/training/intel-firmware-support-package-technical-training.pdf)

![Intel's firmware philosophy](img/intel-firmware-philosophy.png)

## Vendor perspective

> Intel is working towards releasing as much source code as possible going
> forward. A binary component is still the best way to encapsulate the complex
> solution that developers may not necessarily need to bother about as long as
> the binary component does its job right.

source: [FSP whitepaper](https://www.intel.com/content/dam/www/public/us/en/documents/white-papers/fsp-iot-royalty-free-firmware-solution-paper.pdf)

## Dexter's Law

> Only proprietary software vendors want proprietary software.

## Spotting the issue

### Attackers [do not play by the rules](https://youtu.be/WhSrLk6vWgQ?t=1984)

## First steps

![Yellow brick road](img/wizard-of-oz_yellow-brick-road-start.png){ height=80% }

## Previous work / existing resources

### Analysis

- `me_cleaner` and its [wiki](https://github.com/corna/me_cleaner/wiki/)
- [Heads docs on ME cleaner](http://osresearch.net/Clean-the-ME-firmware.html)
- [MEAnalyzer](https://github.com/platomav/MEAnalyzer)

### Reverse engineering

- ROMP module reverse engineering [effort by Youness Alaoui](https://puri.sm/posts/reverse-engineering-the-intel-management-engine-romp-module/)
- [Huffman decoders](https://io.netgarage.org/me/)
- tools by [Positive Research](https://github.com/ptresearch)

### More information

- [talks by Igor Skochinsky](https://github.com/skochinsky/papers)
- [Win-Raid Forum](https://www.win-raid.com/f39-Intel-Management-Engine.html)
- [talk by Intel at Black Hat USA 2019](https://www.youtube.com/watch?v=TsXzDFjXj2s)

## [Plundervolt](https://plundervolt.com/#questions)

![Plundervolt logo](img/plundervolt.png){ height=20% }

> We build on the reverse engineering efforts of [64, 49, 57] that revealed the existence of an undocumented MSR to adjust operating voltage on Intel Core CPUs. To ensure reproducibil- ity of our findings, we document this concealed interface in detail. All results were experimentally confirmed on our test platforms (cf. Table I).

## Security

### Hardware and firmware have to be combined.

[PTT](https://www.intel.com/content/dam/www/public/us/en/documents/white-papers/enterprise-security-platform-trust-technology-white-paper.pdf)
is a TPM 2.0 implementation

### Security has many dimensions.

- physical: voltages, hardware accessibility
    * see Plundervolt
- computational: constant-time for crypto ops
    * see TPM Fail
- logical: programmatic flaws

### Auditability is a requirement, fulfilled by open source.

\begin{theorem}
no audit => no trust
\end{theorem}

# Firmware Analysis

## Firmware Partition Table

:::::::::::::: {.columns}
::: {.column width="75%"}

![FPT](img/me_partitions.png){ width=100% }

:::
::: {.column width="25%"}

- partition `FTPR`
- offset `0x31000`
- size `0x40000`

:::
::::::::::::::

## Code Partition Directory

Each CPD entry can be either:

- partition manifest (".man"), "old" generation 2 manifest
- module metadata (".met"), also contains the module hash
- module

## CPD data structure

see [Win-Raid Forum](https://www.win-raid.com/t596f39-Intel-Management-Engine-Drivers-Firmware-amp-System-Tools-74.html)

:::::::::::::: {.columns}
::: {.column width="75%"}

![CPD](img/cpd_region.png){ width=100% }

:::
::: {.column width="25%"}

- file `FTPR.man`
- offset `0x0088`
- size `0x03f0`

:::
::::::::::::::

## FTPR

- meaning unknown; could refer to _factory_, _partition_, _reset_

### files

- `FTPR.man` - FTPR manifest
- `rbe`
- `rbe.met`
- `manuf`
- `manuf.met`

## FTPR manifest

- seems to consist of three parts (lots of `0000` and `ffff` may be separators)
- header includes architecture (`8086`) and date (`2019-06-17`)
    * followed by the tag `$MN2`
- more metadata? (`FTPR` itself, `rbe`, `manuf`)
- `0x7c`, `0x200200`?

## Trailer?

`rbe`
```
7262 6500 0000 0000 0000 0000 0000 ffff 7c00 0000
```
```
b5da a898 d17c c016 4c04 3b2c f141 c26b
756a de87 dc2c 59b0 995a f551 ac0d e839
```

`manuf`
```
6d61 6e75 6600 0000 0000 0000 0000 ffff 7c00 0000
```
```
9064 981d 6cf7 c15d 9a4a 64aa f081 58cc
2619 a3ae 71ae 6230 8bdb 3694 a7cb 1b83
```

`FTPR`
```
0f00 0000 9c00 0000 4654 5052
```
## And almost the same thing again

`rbe`
```
7262 6500 0000 0000 0000 0000 0002 2000 7c00 0000
```
```
b5da a898 d17c c016 4c04 3b2c f141 c26b
756a de87 dc2c 59b0 995a f551 ac0d e839
```

`manuf`
```
6d61 6e75 6600 0000 0000 0000 0002 2000 7c00 0000
```
```
9064 981d 6cf7 c15d 9a4a 64aa f081 58cc
2619 a3ae 71ae 6230 8bdb 3694 a7cb 1b83
```

`RCHA` - what is that?
```
3200 0000 1000 0000 5243 4841 0000 0000
```

## `manuf`

### consists of three parts

- bootpart
- boot_fpt
- ftpr.mft

## x86 Instructions

`manuf`

```
00000000: 0fa0 66b8 3000 8ee0 b904 0000 0064 8b09  ..f.0........d..
00000010: b800 0000 0064 8b00 ba04 0000 0064 8b12  .....d.......d..
```

:::::::::::::: {.columns height=30%}
::: {.column width="40%"}
```
PUSH FS ; segment register
MOV AX, 0x0030
MOV FS, AX
MOV ECX, 0x000004
MOV ECX,DWORD PTR FS:[ECX]
MOV EAX, 0x000000
```
:::
::: {.column width="60%"}
### References

* [push onto stack](https://c9x.me/x86/html/file_module_x86_id_269.html)
* [16-bit and 8-bit registers](https://wiki.skullsecurity.org/Registers#16-bit_and_8-bit_Registers)
* [single byte or small x86 opcodes](http://xxeo.com/single-byte-or-small-x86-opcodes)
* [x86 assembler in 256 LOC](http://blog.jeff.over.bz/assembly/compilers/jit/2017/01/15/x86-assembler.html)
:::
::::::::::::::

## PMC

- included twice, 65584 bytes - 64KB + 48B (3 * 16B)

### Last three lines

```
00010000: 706d 635f 6677 5f6c 6267 5f62 302d 3138  pmc_fw_lbg_b0-18
00010010: 7777 3334 6100 0000 0000 0000 0000 0137  ww34a..........7
00010020: 0000 0100 0000 0000 0000 0000 0000 0000  ................
```

- probably upper 64KB are actual image and last three lines are meta information
- `pmc_fw_lbg_b0-18ww34a` looks like a version string

## Obtaining ME firmware images

- Lenovo
    * download update, e.g., `https://support.lenovo.com/us/de/downloads/ds503998`
    * run `innoextract [file]` => `app/` directory with files
    * one for consumer and one for corporate version, `Me_xx.x_Coxx.bin` :)
- HP
    * download update, e.g., `h30318.www3.hp.com/pub/softpaq/sp99501-100000/sp99829.exe`
    * run `7z x [file]` (in a new directory) => many files, we want `Q72_xxxxxx.bin`
    * `xxd Q72_xxxxxx.bin | grep "\$FPT"` (extract line with FPT tag)
    * note down address at beginning without `0` at the end, minus `1`
    * `dd if=Q72_xxxxxx.bin bs=16 skip=0x[beginning] count=0x1000 of=me.bin`
    * run `MEA.py` over it: `MEA.py me.bin`
    * check expected length, try higher `count` for `dd` in case of error
    * correct the count and `dd` again => there we go, `me.bin` :)
- [Win-Raid Forum](https://www.win-raid.com/t832f39-Intel-Engine-Firmware-Repositories.html)

# Conclusion

## Security

### All firmware has to be fully open source.

## Abbreviations and Acronyms

+--------+---------------------------------+
| PMC    | Power Management Controller     |
+--------+---------------------------------+
| MSR    | Model-Specific Register         |
+--------+---------------------------------+
| PCR    | Platform Configuration Register |
+--------+---------------------------------+
| FIT(C) | Flash Image Tool                |
+--------+---------------------------------+
| FPT    | Firmware Partition Table        |
+--------+---------------------------------+
| CPD    | Code Partition Directory        |
+--------+---------------------------------+
| RBE    | ROM Boot Extension              |
+--------+---------------------------------+
| DAL    | Dynamic Application Loader      |
+--------+---------------------------------+
| PTT    | Platform Trust Technology       |
+--------+---------------------------------+
| FPF    | Field Programmable Fuse         |
+--------+---------------------------------+

## Related work

### Talks from Black Hat USA 2019

- [Firmware Cartography: Charting the Course for Modern Server Compromise](https://www.youtube.com/watch?v=OwQ9MxGk8zs)
- [Behind the scenes of iOS and Mac Security](https://www.youtube.com/watch?v=3byNNUReyvE)
- [Inside the Apple T2](https://www.youtube.com/watch?v=vRnyasv1qbU)
- [Breaking Through Another Side: Bypassing Firmware Security Boundaries
from Embedded Controller](https://www.youtube.com/watch?v=g-1Y466rDaI)
- [Breaking Samsung's ARM TrustZone](https://www.youtube.com/watch?v=uXH5LJGRwXI&)

### Talks by Alexander Ermolov

- [Safeguarding rootkits: Intel BootGuard](https://2016.zeronights.ru/wp-content/uploads/2017/03/Intel-BootGuard.pdf)

## Kudos

![Chaospott](img/chaospott.png){ height=25% }
![Chaosdorf](img/chaosdorf.png){ height=25% }
![Das Labor](img/das-labor.png){ height=25% }
![Chaos-West](img/chaos-west.png){ height=25% }

![coreboot](img/coreboot.png){ height=25% }
![LinuxBoot](img/linuxboot.png){ height=25% }
![u-root](img/u-root.png){ height=25% }
![OSFC](img/osfc-oscar.png){ height=25% }

## Thanks!

![Goodbye](img/wizard-of-oz_goodbye.png){ height=85% }

## Questions?

[https://github.com/orangecms/look-at-me](https://github.com/orangecms/look-at-me)

[https://metaspora.org/look-at-me.pdf](https://metaspora.org/look-at-me.pdf)
