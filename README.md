# ArxmlDataExtractor

ArxmlDataExtractor makes it easy for everybody to extract data from an AUTOSAR .arxml file. It uses common .yaml files as data extraction specification, afterward referred to as configuration file. It supports the extraction of complex data structures as well as the handling of AUTOSAR references. The extracted data can then be written into three formats: '.txt', '.json' and '.xlsx'.

## Supported Features

- Simple syntax to describe data extraction
- Supports XPath expression with auto-handling of AUTOSAR namespaces
- Supports extracting data from AUTOSAR References
- Specify the output data structure within the configuration
- Value conversion into integer, float or date
- Config files can be shared and reused
- Simple data output in a .txt file for rapid prototyping
- JSON output for reusing the data in other scripts or tools
- Excel output for better analytics support like filtering or sorting

## Usage

In order to extract data from a given ARXML file, ArxmlDataExtractor.exe needs to be called with the following syntax in your command window.

```batch
ArxmlDataExtractor.exe [-h] --config CONFIG --input INPUT --output OUTPUT
```

The order of the options is optional and can be rearranged. The table below describes the available options.

| Short| Option   | Description                                                  |
|------|----------|--------------------------------------------------------------|
|  -h  | --help   | show help message                                            |
|  -c  | --config | config file that specified the data that should be extracted |
|  -i  | --input  | ARXML file from where the data should be extracted           |
|  -o  | --output | output file, possible formats are: .txt, .json or .xlsx      |
|  -d  | --debug  | enables debug mode, will write a .log file                   |

## Configuration File

### Structure

In general, every configuration file will consist of objects and values. An object is a collection of values with a given name and an anchor. Value describes the data to be extracted from the ARXML file. It consists of a freely chosen name and additional parsing instructions in the following referred to as queries.

Every configuration file has one thing in common. It has to start with at least one object. This object will the entry point, specified by one of the allowed anchors, and will be the entry point for the following values.
This is used to optimize query processing and therefore the parsing performance. Each query will use the anchor of its parent object as a base. The parsing instructions will be handled relatively starting from this base. Important note, an anchor can either return a single object (if only one element exists in the ARXML) or a list of all matching elements.

```yaml
Object:
  anchor: <...>
  value: <...>
  ...
```

Below is a simple example of a configuration specification that extracts all top-level 'AR-PACKAGE' elements from the given '.arxml' file. The root object is called 'Package' with an XPath expression as an anchor. The anchor will return a list of all elements named 'AR-PACKAGE' with a parent element named 'AR-PACKAGES' started from the root element ('AUTOSAR'). More information about XPath expression can be found [here](https://www.w3schools.com/xml/xpath_syntax.asp)). More information about anchors and their types can be found in the Anchor section.

```yaml
Package:
  _xpath: "./AR-PACKAGES/AR-PACKAGE"
  Name: "SHORT-NAME"
```

Underneath the anchor, the values are specified. In this case, there's only one value defined with the name 'Name'. The query for this value refers to a child element named 'SHORT-NAME'. This element is the child of the defined anchor in this case, 'AR-PACKAGE'. The query can be interpreted as:
>From the object's base, go to its child element 'SHORT-NAME', extract the text value and write in a variable called 'Name' contained in the object called 'Package'.

### Nesting Objects

With nesting objects, the data structure of the output data can be defined. Besides, if used cleverly, the parsing time can be reduced. This will be relevant if you want to extract multiple values from a common child element. Because every object has an anchor, it can be set to the common child to reduce the parsing depth.

```yaml
object1:
  anchor: <...>
  value1: <...>
  object2:
    anchor: <...>
    value2: <...>
```

The following configuration shows a concrete example of nesting objects. Let's assume you want to list all PDUs and their timing specification from an ECU extract. Therefore, you can create a root object for finding all PDUs and add a nested object for the timing specification. The queries for the values of 'MinimumDelay' and 'CyclicTiming' will use the anchor of the object 'Timing Specification' as their base element.

```yaml
PDU:
  _xpath: ".//I-SIGNAL-I-PDU"
  Name: "SHORT-NAME"
  TimingSpecification:
    _xpath: "./*/I-PDU-TIMING"
    MinimumDelay: "MINIMUM-DELAY"
    CyclicTiming: "TRANSMISSION-MODE-DECLARATION/TRANSMISSION-MODE-TRUE-TIMING/CYCLIC-TIMING/TIME-PERIOD/VALUE"
```

You can also extract that information without nested objects. Then the values will be part of the PDU object and the parsing time can increase slightly.

### Advanced Value Handling

Value queries can be further refined by specifying the extract location and format. This can be done by prepending additional parsing information to the path. This is optional and will default to the text property of the found element specified by the path in the string format.

```yaml
value: [location[>format]:]<xpath-to-element>
```

Important to know is that if a format conversion is added, then also the value location needs to be set. To separate the location from the format `>` will be put in between. To further separate the parsing instructions from the path, they will be split by `:`. The following configuration extends the PDU extraction example to also convert the timing specification values in their proper format. 'MinimumDelay' will be converted to an integer and 'CyclicTiming' to a float value.

```yaml
PDU:
  _xpath: ".//I-SIGNAL-I-PDU"
  Name: "SHORT-NAME"
  TimingSpecification:
    _xpath: "./*/I-PDU-TIMING"
    MinimumDelay: "text>int:MINIMUM-DELAY"
    CyclicTiming: "text>float:TRANSMISSION-MODE-DECLARATION/TRANSMISSION-MODE-TRUE-TIMING/CYCLIC-TIMING/TIME-PERIOD/VALUE"
```

If the conversion isn't possible, it will default to its textual representation. More information about the values' location and format can be found in the Syntax section.

### Syntax

#### Object Anchors

An object anchor is the entry point for all following value queries. The anchor is used to find the specified XML elements, e.g. all top-level 'AR-PACKAGE' elements. Therefore the anchor needs to describe where to find those elements. The following types of anchors are supported.

| Syntax | Description                                                                   | Usage                                              |
|--------|-------------------------------------------------------------------------------|----------------------------------------------------|
| _xpath | Any XPath expression can be used to specify the object that should be parsed  | `_xpath: ./AR-PACKAGES/AR-PACKAGE`                 |
| _ref   | AUTOSAR Reference to a specific object                                        | `_ref: /PDU/Name`                                  |
| _xref  | Any XPath expression that leeds to an element containing an AUTOSAR Reference | `_xref: .//I-SIGNAL-TO-I-PDU-MAPPING/I-SIGNAL-REF` |

The `_xref` anchor is a special type of anchor because it is a combination of both `_xpath` and `_ref`. This is handy if you want to get data from element but from the current context, you only have access to its AUTOSAR reference. An easy example would be if you want the data type of a signal that is mapped to a PDU. The PDU only contains a reference to the signal, so to get the signals data type you need to look at the signal element itself.

How does this work? First, it tries to find the element containing the AUTOSAR reference specified by the XPath. Then it grabs the reference from the elements text value and looks up the referred element which then will be the base for the child value queries.

This is coming very handy if multiple values from the referenced element should be extracted. If so, the expression will only be executed once and the referenced element will be cached for all the following queries. If only one value is required of a reference than an inline reference can be used (next section).

#### Value Path

A values' path consists of an XPath expression that leads to the element where the data can be found. All types of XPath expressions can be used. Optionally, the path can be converted into an inline reference by prepending `&(<xpath-to-ref>)` to the actual XPath expression.

```yaml
value: [&(<xpath-to-ref>)]<xpath-to-element>
```

An inline reference is a combination of an XPath expression with an AUTOSAR reference. If the path of a value query starts with a `&`, it indicates that the path should be interpreted as inline reference. `<xpath-to-ref>` contains the XPath expression to the element containing the AUTOSAR reference in its text property. `<xpath-to-element>` is the XPath expression to the actual value location, using the referenced element as a base.

```yaml
PDU:
  _xpath: ".//I-SIGNAL-I-PDU"
  Name: "SHORT-NAME"
  Signal:
    _xpath: "//I-SIGNAL-TO-I-PDU-MAPPING"
    Name: "&(I-SIGNAL-REF)SHORT-NAME"
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
| `string` | Takes the textual representation   | `value: text>string:<xpath>`|
| `int`    | Converts the value into an integer | `value: text>int:<xpath>`   |
| `float`  | Converts the value into float      | `value: text>float:<xpath>` |
| `date`   | Converts the value into a date     | `value: text>date:<xpath>`  |

### Example Configuration

Example configurations can be executed with the provided .arxml file.

#### Get PDU Information

This .yaml configuration will parse all PDUs present in the given .arxml file and extract the specified values. It will automatically handle situations where a PDU contains multiple signals. Therefore, all Signals will be extracted and reported.

```yaml
PDU:
  _xpath: ".//I-SIGNAL-I-PDU"
  Name: "SHORT-NAME"
  Length: "text>int:LENGTH"
  CyclicTiming: "text>float:.//TRANSMISSION-MODE-TRUE-TIMING/CYCLIC-TIMING/TIME-PERIOD/VALUE"
  SignalMappings:
    _xpath: ".//I-SIGNAL-TO-I-PDU-MAPPING"
    Signal: "SHORT-NAME"
    StartPosition: "text>int:START-POSITION"
    ISignal:
      _xref: "I-SIGNAL-REF"
      InitValue: "text>int:.//VALUE"
      Length: "text>int:LENGTH"
```

#### Get CAN Cluster Specification

This configuration uses an AUTOSAR Reference to get the information of the CAN Cluster. Please note, that the reference will change whenever the CAN Cluster will be renamed. You should have that in mind if you think of reusing the script. AUTOSAR References will be fast for prototyping but if you want to reuse the configuration you should aim for XPath expressions.

```yaml
CanCluster:
  _ref: "/Cluster/CAN"
  Name: "SHORT-NAME"
  Baudrate: "text>int:CAN-CLUSTER-VARIANTS/CAN-CLUSTER-CONDITIONAL/BAUDRATE"
  LongName: "text:LONG-NAME/L-4"
  Language: "@L:LONG-NAME/L-4"
```
