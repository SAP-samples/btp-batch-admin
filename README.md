[![REUSE status](https://api.reuse.software/badge/github.com/SAP-samples/cloud-sfsf-benefits-ext)](https://api.reuse.software/info/github.com/SAP-samples/cloud-sfsf-benefits-ext)

# Cloud Managment Batch
Simple CloudFoundry Multi-Target-Application with BASH based batch files for creating/deleting/deploying via the btp command.

## Description

This repo contains a complete example of interacting with the BTP CLI tool.  It take the form of multi-target application(MTA) with a set of bash based batch files found in the tools folder.  

This example is referred to in an upcoming blog post.: [Blog Post](https://people.sap.com/andrew.lunde#content:blogposts)

## Requirements

- The user is expected to be familiar BASH Batch programming.


## Download and Installation

>  **Note:**  These instructions assume you are using a Linux or MacOS system or Business Application Studio(BAS).  If you are on Windows, substitute "/" for "\\" in the included commands.


## Limitations

This example is intended to illustrate the use of the BTP command-line tool in a batch context.  It does not contain extensive error handling or enforce a certain order of operations.  As such, certain assumptions apply and key values are hard coded.  For instance, you need to obtain and set values in the #GLOBAL VALUES section near the top of each batch file.

## Known Issues

This example contains no known issues.

## How to obtain support

This project is provided "as-is" with no expectation for major changes or support.

## To-Do (upcoming changes)

Documentation of the underlying API may promote removal of certain "work-around" sections of the batch files.

## License
Copyright (c) 2021 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE file](LICENSES/Apache-2.0.txt).