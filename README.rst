|License|


siibra neuroimaging toolbox
=============================

Copyright 2020-2021, Forschungszentrum Jülich GmbH

*Authors: Big Data Analytics Group, Institute of Neuroscience and
Medicine (INM-1), Forschungszentrum Jülich GmbH*


This repository provides a toolbox for `siibra <https://siibra-python.readthedocs.io>`__ which provides functionalities to assign whole brain activation maps, as obtained from functional neuroimaging, to brain regions. Given an input volume in the form of a NIfTI file, the toolbox will segregate the input signal into connectec components, and then analyze overlap and correlation of each component with regions defined in an atlas. Per default, the Julich-Brain probabilistic cytoarchitectonic maps defined in MNI152 space are used, and the input volume is assumed in the same physical space. The functionality is strongly inspired by similar functionalities of the popular `SPM anatomy toolbox <https://github.com/inm7/jubrain-anatomy-toolbox>`__ [EickhoffEtAl2005]_.

In the current implementation, it provides a Python library as well as an extension to the `siibra-cli <https://github.com/FZJ-INM1-BDA/siibra-cli>`__ commandline client. The result is a formatted report about brain regions that overlap with strong signals and their properties. Future versions will provide an interactive plugin to `siibra-explorer <https://github.com/FZJ-INM1-BDA/siibra-explorer>`__, the interactive web browser hosted at <https://atlases.ebrains.eu/viewer/go/human>. 
 
  **Note** that ``siibra-toolbox-neuroimaging`` is still in early development. Get in touch with us to discuss, and feel free to post issues here on github.


The toolbox relies on the functionalities of ``siibra-python``, documented at https://siibra-python.readthedocs.io. It includes a catalogue of well
documented code examples that walk you through the different concepts
and functionalities. As a new user, it is recommended to go through
these examples - they are easy and will quickly provide you with the
right code snippets that get you started. 

References
----------

.. [EickhoffEtAl2005] Eickhoff S, Stephan KE, Mohlberg H, Grefkes C, Fink GR, Amunts K, Zilles K: A new SPM toolbox for combining probabilistic cytoarchitectonic maps and functional imaging data. NeuroImage 25(4), 1325-1335, 2005


Acknowledgements
----------------

This software code is funded from the European Union’s Horizon 2020
Framework Programme for Research and Innovation under the Specific Grant
Agreement No. 945539 (Human Brain Project SGA3).

.. acknowledgments-end

.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0
