# 2018 Undergraduate Summer Research at the University of Manitoba
Given the increasing need of fault detection and diagnosis and the decreasing feasibility of manual condition monitoring nowadays, this project focused on the development of a modular device that can be retrofitted onto existing machines to monitor their performance. The data are stored on the device and then automatically sent to a cloud server when a wireless connection is established. Once on the cloud server, it can be downloaded and analyzed from anywhere in the world.

The code was written in Python 3 and used Amazon Web Services to store data. Work was done at the University of Manitoba'a Fluid Power and TeleRobotics Research Laboratory

The DAQ file is ran locally on the modular device and the Conversion File is ran on any host computer that will be retrieving the data.

![modular device](https://user-images.githubusercontent.com/43504838/50371050-35de2780-0568-11e9-9fa4-04ba7a3fa3cf.jpg)

The modular Device Consisted of a Raspberry Pi 3, and basic circuitry to step down voltage signals and filter noise


![tractor](https://user-images.githubusercontent.com/43504838/50371085-b8ff7d80-0568-11e9-801b-d59050e81631.png)
![tractor 2](https://user-images.githubusercontent.com/43504838/50371086-b9981400-0568-11e9-9186-95f7b004f2f6.jpg)

The device was tested on an agriculture tracotr and succesfully sampled and stored data in regards to the pressure cylinders controlling the steering of the machine.
