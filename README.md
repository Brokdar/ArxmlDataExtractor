# ArxmlDataExtractor

ArxmlDataExtractor makes it easy for everybody to extract data from an AUTOSAR .arxml file. It uses common .yaml files as data extraction specification, afterwards referred as configuration file. It supports extraction of complex data structures as well as handling of AUTOSAR references. The extracted data can then be written into three formats: .txt, .json and .xlsx.

## Supported Features

- Simple syntax to described which data should be extracted
- Supports XPath expression with auto-handling of AUTOSAR namespaces
- Value conversion into integer, float or date
- Supports extracting data from AUTOSAR References
- Config files can be shared and reused
- Specify data structure within the configuration
- Simple data output in a .txt file for rapid prototyping
- JSON output for reusing the data in other scripts / tools
- Excel output for better analytics support

## Usage

In order to extract data from a given ARXML file, just call ArxmlDataExtractor.exe with the following syntax in your command window. The order of the options is optional and can be rearranged.

```batch
ArxmlDataExtractor.exe [-h] --config CONFIG --input INPUT --output OUTPUT
```

| Short| Option   | Description                                                  |
|------|----------|--------------------------------------------------------------|
|  -h  | --help   | show help message                                            |
|  -c  | --config | config file that specified the data that should be extracted |
|  -i  | --input  | ARXML file from where the data should be extracted           |
|  -o  | --output | output file, possible formats are: .txt, .json or .xlsx      |

## Configuration File

### Structure

In general, every configuration file will consist of objects and values. An object is a collection of values with a given name and an anchor. A value describes the data to be extracted from the ARXML file. It consists of a freely chosen name and additional parsing instructions.

Every configuration file has one thing in common. It has to start with at least one object. The object contains only one of the allowed anchors and will be the entry point of the following values. This is used to optimize query processes and therefore the parsing performance. The parsing instructions of a value uses the anchor element of the parent object as a base. An anchor can either return a single object (if only one found in the ARXML) or a list of all objects matching the expression.

```yaml
Object:
  anchor: <...>
  value: <...>
  ...
```

Below a simple example of a configuration that extracts all top-level AR-PACKAGES in a given ARXML file. It starts with the object 'Package'. It's anchor is an XPath instruction to list all elements which can be found by the expression (More information about XPath can be found [here](https://www.w3schools.com/xml/xpath_syntax.asp)). The Object Anchor section contains a detailed description about the available anchors. Withing the object (intended) the value is specified. In this case the values name is 'Name' and it refers to the objects child element 'SHORT-NAME'. This instruction read as the following: Go from the objects base to its child 'SHORT-NAME' and write the text value in the Package.Name variable.

```yaml
Package:
  _xpath: ./AR-PACKAGES/AR-PACKAGE
  Name: SHORT-NAME
```

### Nesting Objects

Nesting objects allows for better data structure and further improvements in parsing time. For example, if you want to list all PDUs and their Timining Specifications you can use nested objects to structure the extracted data as following. Please note, that each object needs its own anchor.

```yaml
object1:
  anchor: <...>
  value1: <...>
  object2:
    anchor: <...>
    value2: <...>
```

This has an additional advantage in performance because both values are children of the 'I-PDU-TIMING' element. The expression to find this value (specified by the anchor) will only be executed once. The found element will then be used as base for the values 'MinimumDelay' and 'CyclicTiming'.

```yaml
PDU:
  _xpath: .//I-SIGNAL-I-PDU
  Name: SHORT-NAME
  TimingSpecification:
    _xpath: ./*/I-PDU-TIMING
    MinimumDelay: MINIMUM-DELAY
    CyclicTiming: TRANSMISSION-MODE-DECLARATION/TRANSMISSION-MODE-TRUE-TIMING/CYCLIC-TIMING/TIME-PERIOD/VALUE
```

### Advanced Value Handling

A value has some special treatments when it comes to where to extract it from and in which format. Therefore, in addition to the path, you can specify the location and the format. Both values are totally optional and default to the text property of the element specified by the path. If a format is provided, then also the location of the property has to be given. It's very important to also add the `>` between the location and the format. It will tell the tool that the data by the location will be converted into specified format. After the value information a `:` is required to separate the value information from the value path.

Note: if the conversion isn't possible the tool will raise an exception. So be careful when to use the format conversion, double check if the value you want to extract can be converted into that format. Possible locations and format can be found in the Syntax section.

```yaml
value: [location[>format]:]<xpath-to-element>
```

Example of value conversion into different formats.

```yaml
PDU:
  _xpath: .//I-SIGNAL-I-PDU
  Name: SHORT-NAME
  TimingSpecification:
    _xpath: ./*/I-PDU-TIMING
    MinimumDelay: text>int:MINIMUM-DELAY
    CyclicTiming: text>float:TRANSMISSION-MODE-DECLARATION/TRANSMISSION-MODE-TRUE-TIMING/CYCLIC-TIMING/TIME-PERIOD/VALUE
```

### Syntax

#### Object Anchors

An object anchor is the entry point for all child values of the object itself. The anchor is used to find the specified object e.g. all top-level AR-PACKAGE elements. Therefore the anchor needs to describe where to find those elements. The following type of anchors are supported.

| Syntax | Description                                                                   | Usage                                              |
|--------|-------------------------------------------------------------------------------|----------------------------------------------------|
| _xpath | Any XPath expression can be used to specify the object that should be parsed  | `_xpath: ./AR-PACKAGES/AR-PACKAGE`                 |
| _ref   | AUTOSAR Reference to a specific object                                        | `_ref: /PDU/Name`                                  |
| _xref  | Any XPath expression that leeds to an element containing an AUTOSAR Reference | `_xref: .//I-SIGNAL-TO-I-PDU-MAPPING/I-SIGNAL-REF` |

The `_xref` anchor is a special type of anchor. It is a combination of both `_xpath` and `_ref`. First it tries to find the value specified by the XPath and then it grabs the AUTOSAR Path and looks up the referred element. This is coming very handy if multiple values from the referenced object should be extracted. If so, the XPath expression will only be executed onces and the referenced element will be cached for all the following values. If only one value is required of a reference than this can be achieved with a reference path.

#### Value Path

A values' path consists of a XPath expression that leads to the element where the data should be extracted from.

You can also add the inline reference operator `&` to tell the tool that the XPath expression leads to an AUTOSAR reference from where the data should be extracted from. The tool will then execute the XPath expression and afterwards go to the AUTOSAR Reference and extract the data from there.

```yaml
value: [&(<xpath-to-ref>)]<xpath-to-element>
```

```yaml
Name: &(I-SIGNAL-REF)SHORT-NAME
```

#### Value Location

| Syntax    | Description                               | Usage                  |
|-----------|-------------------------------------------|------------------------|
| `tag`     | Gets the tag of the element               | `value: tag:<xpath>`   |
| `text`    | Gets the text of the element              | `value: text:<xpath>`  |
| `@<name>` | Gets the value of the specified attribute | `value: @UUID:<xpath>` |

#### Value Formats

| Syntax   | Description                        | Usage                       |
|----------|------------------------------------|-----------------------------|
| `string` | Don't converts the value           | `value: text>string:<xpath>`|
| `int`    | Converts the value into an integer | `value: text>int:<xpath>`   |
| `float`  | Converts the value into float      | `value: text>float:<xpath>` |
| `date`   | Converts the value into a date     | `value: text>date:<xpath>`  |

### Example Configuration

Example configurations can be executed with the provided .arxml file.

#### Get PDU Information

This .yaml configuration will parse all PDUs present in the given .arxml file and extract the specified values. It will automatically handle situations where a PDU contains multiple signals. Therefore, all Signals will be extracted and reported.

```yaml
PDU:
  _xpath: .//I-SIGNAL-I-PDU
  Name: SHORT-NAME
  Length: text>int:LENGTH
  CyclicTiming: text>float:.//TRANSMISSION-MODE-TRUE-TIMING/CYCLIC-TIMING/TIME-PERIOD/VALUE
  SignalMappings:
    _xpath: .//I-SIGNAL-TO-I-PDU-MAPPING
    Signal: SHORT-NAME
    StartPosition: text>int:START-POSITION
    ISignal:
      _xref: I-SIGNAL-REF
      InitValue: text>int:.//VALUE
      Length: text>int:LENGTH
```

#### Get CAN Cluster Specification

This configuration uses an AUTOSAR Reference to get the information of the CAN Cluster. Please note, that the reference will change whenever the CAN Cluster will be renamed. You should have that in mind if you think of reusing the script. AUTOSAR References will be fast for prototyping but if you want to reuse the configuration you should aim for XPath expressions.

```yaml
CanCluster:
  _ref: /Cluster/CAN
  Name: SHORT-NAME
  Baudrate: text>int:CAN-CLUSTER-VARIANTS/CAN-CLUSTER-CONDITIONAL/BAUDRATE
  LongName: text:LONG-NAME/L-4
  Language: @L:LONG-NAME/L-4
```
