# CPP_High-Res_fMRI

This is a set of functions to analyses High Res fMRI data

This can perform:

- [ W I P ]

The core functions are in the `src` folder. This set of functions is intended to be added manually
as a submodule to the analysis repo forked from
[template_datalad_fMRI](https://github.com/cpp-lln-lab/template_datalad_fMRI)

## How to install and use this template

### Add as a submodule

1. Open the terminal and navigate to your analysis folder forked from
[template_datalad_fMRI](https://github.com/cpp-lln-lab/template_datalad_fMRI) and cloned locally

2. Type

```bash
# navigate to the `lib` folder
cd lib

# add the submodule
git submodule add https://github.com/cpp-lln-lab/CPP_High-Res_fMRI.git

# initialize the nested submodule(s)
git submodule update --init --recursive
```

3. commit the new changes (the new submodule(s))

### Dependencies

Make sure that the following toolboxes are installed
path.

For instructions see the following links:

<!-- lint disable -->

| Dependencies                                                                              | Used version         |
| ----------------------------------------------------------------------------------------- | ---------------------|
| [Matlab](https://www.mathworks.com/products/matlab.html)                                  | 2017b                |
| or [octave](https://www.gnu.org/software/octave/)                                         | 4.?                  |
| [SPM12](https://www.fil.ion.ucl.ac.uk/spm/software/spm12/)                                | v7487                |
| [CPP_SPM](https://github.com/cpp-lln-lab/CPP_SPM)*                                        | > 1.1.3              |
| [Afni](https://afni.nimh.nih.gov/)                                                        | AFNI_21.2.00 'Nerva' |
| [LayNii](https://github.com/layerfMRI/LAYNII)                                             |  2.2.0               |

\*already "installed" in [template_datalad_fMRI](https://github.com/cpp-lln-lab/template_datalad_fMRI) and cloned locally

<!-- lint enable -->

## Contributing

Feel free to open issues to report a bug and ask for improvements.

If you want to contribute, have a look at our
[contributing guidelines](https://github.com/cpp-lln-lab/.github/blob/main/CONTRIBUTING.md)
that are meant to guide you and help you get started. If something is not clear
or you get stuck: it is more likely we did not do good enough a job at
explaining things. So do not hesitate to open an issue, just to ask for
clarification.
