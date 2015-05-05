# Book Outline Generator

Create the notes outline file for a book.

I use this when I start reading a new book.  Check my [notes](https://github.com/tedmiston/notes) repo for real-life examples.

## Features

- Supports one or many authors (with optional homepage urls)
- Creates a numbered, hyperlinked table of contents
- Adds *TODO* stubs to indicate which chapters you haven't read
- Adds *back to top* link after each chapter

## Installation

Inside a virtual environment:

```
$ pip install -r requirements.txt
```

## Quickstart

To generate an outline:

```
$ python bog.py <input-file>
```

For example, to generate an outline for 37signals' wonderful book [REMOTE](http://37signals.com/remote/):

```
$ python bog.py outlines/remote.yaml
```

The input yaml file should look like:

```yaml
title    : Remote
subtitle : Office Not Required
url      : http://37signals.com/remote/

authors  : 
  - name : Jason Fried
    url  : https://signalvnoise.com/writers/jf
  - name : David Heinemeier Hansson
    url  : http://david.heinemeierhansson.com/

sections :
  - .Introduction
  - The Time is Right for Remote Work
  - Dealing with Excuses
  - How to Collaborate Remotely
  - Beware the Dragons
  - Hiring and Keeping the Best
  - Managing Remote Workers
  - Life as a Remote Worker
  - .Conclusion
  - .The Remote Toolbox
```

*Note that chapters prefixed with a `.` will not be numbered in the output.*

The output markdown file:

```md
# Remote
*Office Not Required*<br>
by [Jason Fried](https://signalvnoise.com/writers/jf), [David Heinemeier Hansson](http://david.heinemeierhansson.com/)

---

**Table of Contents**

- [Introduction](#pre1)
- [1. The Time is Right for Remote Work](#ch1)
- [2. Dealing with Excuses](#ch2)
- [3. How to Collaborate Remotely](#ch3)
- [4. Beware the Dragons](#ch4)
- [5. Hiring and Keeping the Best](#ch5)
- [6. Managing Remote Workers](#ch6)
- [7. Life as a Remote Worker](#ch7)
- [Conclusion](#post1)
- [The Remote Toolbox](#post2)

---

## <a name="pre1"></a>Introduction

- TODO

<sub><sup>[back to top](#)</sub></sup>


## <a name="ch1"></a>1. The Time is Right for Remote Work

- TODO

<sub><sup>[back to top](#)</sub></sup>


## <a name="ch2"></a>2. Dealing with Excuses

- TODO

<sub><sup>[back to top](#)</sub></sup>


## <a name="ch3"></a>3. How to Collaborate Remotely

- TODO

<sub><sup>[back to top](#)</sub></sup>


## <a name="ch4"></a>4. Beware the Dragons

- TODO

<sub><sup>[back to top](#)</sub></sup>


## <a name="ch5"></a>5. Hiring and Keeping the Best

- TODO

<sub><sup>[back to top](#)</sub></sup>


## <a name="ch6"></a>6. Managing Remote Workers

- TODO

<sub><sup>[back to top](#)</sub></sup>


## <a name="ch7"></a>7. Life as a Remote Worker

- TODO

<sub><sup>[back to top](#)</sub></sup>


## <a name="post1"></a>Conclusion

- TODO

<sub><sup>[back to top](#)</sub></sup>


## <a name="post2"></a>The Remote Toolbox

- TODO

<sub><sup>[back to top](#)</sub></sup>
```

Then replace TODOs with your notes as you read.

You can use the outline files provided in `outlines` or follow their syntax to create your own (pull requests welcome).
