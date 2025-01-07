# Text-To-Relations 

**Text-To-Relations: a tool for Information and Relation Extraction**

First, Text-To-Relations lets you perform **entity recognition** by providing a simple interface for creating complex regular expressions.
- If you regularly find yourself writing complex regular expressions, the project can be used as a utility for quickly writing a first draft and easily testing it out.

Then you can combine these entities to form **relations** with Text-To-Relations's abstract base class and the working example provided.

Text-To-Relations has been tested on:
- Python 3.9.18 and Python 3.11.6 on MacOS Sequoia 15.2
- Python 3.10.12 on Ubuntu 22

We expect it to work without issue in many other environments as well.

Source code at [GitHub text_to_relations](https://github.com/jkurlandski01/text_to_relations).

## Installation Instructions

After setting up your virtual environment, install Text-To-Relations with this Pip command.
```
pip install text_to_relations
```

If your Python version is less than 3.11, upgrade pip and install typing_extensions:
```
pip install --upgrade pip

pip install typing_extensions
```

Text-To-Relations also requires Spacy.  Install the Spacy dependencies with these commands. As far as we know, Text-To-Relations is agnostic with regard to the specific Spacy version.

```
pip install -U spacy

python -m spacy download en_core_web_lg
```


## A Tutorial

### Entity Recognition

For this example we're going to write rules to extract postage stamp descriptions as found at https://www.mysticstamp.com/.

Here is Python code to create an input string containing the descriptions for several 19th Century U.S. postage stamps.

```python
import inspect

input = \
"""
# 11A - 1853-55 3¢ George Washington, dull red, type II, imperf

# 17 - 1851 12c Washington imperforate, black

# 12 - 1856 5c Jefferson, red brown, type I, imperforate

# 18 - 1861 1c Franklin, type I, perf 15

# 40 - 1875 1c Franklin, bright blue

# 42 - 1875 5c Jefferson, orange brown

# 62B - 1861 10c Washington, dark green

input = inspect.cleandoc(input)
"""
```

We'll break the first description up into its constituent parts:
- id: *# 11A*
- year_issued: *1853-55*
- value: *3*
- denomination: *cents*
- theme: *George Washington*
- color: *dull red*
- type: *II*
- perforation_info: *imperforate*

Let's pretend that our goal is to write rules to successfully process all the data at the Mystic Stamp website. We hope that writing rules for these examples will give us a good start.

### RegexString

With Text-To-Relations, the go-to tool is RegexString, which is essentially a wrapper around your basic regular expression. The wrapper lets you construct highly useful, working regular expressions with little or no fuss--and requiring from you a minimum amount of understanding the arcane details of regular expressions.

The simplest interface is RegexString's constructor, which with default parameters just takes a list of strings which you want to be considered "synonymous" in some way, that is, as different examples of the same kind of thing.

#### Example 1

We'll use the *type* entity to begin our demonstration of RegexString. In the text above you see that there are only two--"type I" and "type II". But let's suppose that, in the complete data on the website:
- First, that sometimes the word *type* is capitalized and sometimes it is all-lowercase.
- Second, that the types run from Roman numeral I through V.

```python
type_markers = ['type', 'Type']
type_rs = RegexString(type_markers, whole_word=True)
print(f"Regular expression for 'type_rs': {type_rs.get_regex_str()}\n")

roman_numerals = ['I', 'II', 'III', 'IV', 'V']
roman_nums_rs = RegexString(roman_numerals, whole_word=True)
print(f"Regular expression for 'roman_nums_rs': {roman_nums_rs.get_regex_str()}")
```

If you ran the code above you would see this as output:

```console
Regular expression for 'type_rs': \b(?:type|Type)\b

Regular expression for 'roman_nums_rs': \b(?:III|II|IV|I|V)\b
```
Both "\btype\b" and "\b(?:III|II|IV|I|V)\b" are valid regular expressions that you could use with the Python `re` regular expression library, for example `re.finditer()` or any other one of the library's functions.

Both regular expressions begin and end with '\b,' which is regex-speak for "whole word only." This is controlled by the `whole_word` parameter, whose default value is False.

The meat of the regex for `roman_nums_rs` consists of the five Roman numerals separated by "|" (meaning OR), which will match on any one of the five if found in a piece of text. Some other things to note here:
- The regular expression sorts the OR'd numerals by length so that, for example, if "II" occurs in the text you will get a single match on the entire string rather than two matches on "I." (Note that this is only an issue when `whole_word` is set to False.)
- The scary looking "?:" at the start of the block tells the regular expression matcher not to perform grouping on the match. If you don't know what this means--don't worry, you don't need to know. For most *natural language* processing tasks (as opposed to some text processing tasks), you don't need grouping. Text-To-Relations employs non-capturing by default so that some of the other functionality that builds on RegexString objects can assume the associated regular expression is non-capturing. (If you must have capturing, create the RegeString with `non_capturing=False` to allow capturing.)

Finally we're ready to run our RegexString objects against the stamp descriptions at top.

```python
type_phrase_rs = RegexString.concat_with_word_distances(type_rs, 
                                                        roman_nums_rs,
                                                        min_nbr_words=0, 
                                                        max_nbr_words=0)
matchStrs = type_phrase_rs.get_match_triples(input)
print("\nType info found in the input:")
print(matchStrs)
```
RegexString.concat_with_word_distances() takes two RegexString objects and creates a new RegexString which will match text satisfying both of the original regular expressions when they are within a certain amount of word distance. In our case we are saying that we don't want to allow any words between them. (Note that this is a static function belonging to the RegexString class rather than to any particular RegexSting object.)

When we run this code we see this output:
```console
Type info found in the input:
[('type II', 48, 55), ('type I', 149, 155), ('type I', 195, 201)]
```

get_match_triples( ) runs a MatchString object's regular expression against user-supplied text input. The "triples" it returns are: (1) the matched string; (2) the matched string's starting offset in the input text; and (3) the matched string's ending offset in the input text. 

You see that the `type_phrase_rs` object which we constructed from smaller pieces managed to find all three "type" expressions in the postage stamp input.


#### Example 2

Now let's extract the value of the postage stamp, which will give us a chance to demo RegexString's `prepend` parameter. Our description above has six unique values, only one of which uses the old-fashioned cents character, '¢'. These are: 3¢, 12c, 5c, 1c, 1c, 5c, 10c.

```python
cent_symbols = ['c', '¢']
# Use `prepend` to look for one or two digits before the cent symbol.
cent_rs = RegexString(cent_symbols, prepend='\d\d?')
print(f"\nRegular expression for 'cent_rs': {cent_rs.get_regex_str()}")
matchStrs = cent_rs.get_match_triples(input)
print("\nCents info found in the input:")
print(matchStrs)
```

This outputs:
```console
Regular expression for 'cent_rs': \d\d?(?:c|¢)

Cents info found in the input:
[('3¢', 16, 18), ('12c', 77, 80), ('5c', 124, 126), ('1c', 182, 184), ('1c', 224, 226), ('5c', 262, 264), ('10c', 303, 306)]
```

As a side note, Text-to-Relations offers at least one other way of accomplishing the same goal: we could have created two RegexString objects and then concatenated them with the RegexString concat( ) function.

#### Example 3

Here's one more "Introduction-to-RegexString" example, this time used to extract the perforation information in our postage stamp descriptions. The specific perforation examples we're targeting are: imperf, imperforate, perf 15.

```python
perforation_markers = ['perf', 'imperforate', 'imperf']
perforations_rs = RegexString(perforation_markers)
matchStrs = perforations_rs.get_match_triples(input)
print("\nPerforation info:")
print(matchStrs)
```

When run, the code above gives us:
```console
Perforation info:
[('imperf', 57, 63), ('imperforate', 92, 103), ('imperforate', 157, 168), ('perf', 203, 207)]
```

But this isn't quite what we want. If perforated, the description includes the perforation size. Let's try again.

```python
imperforated_markers = ['imperforate', 'imperf']
imperf_rs = RegexString(imperforated_markers)
matchStrs = imperf_rs.get_match_triples(input)
print("\nImperforated:")
print(matchStrs)

perforation_markers = ['perf']
perf_rs = RegexString(perforation_markers, append=' \d\d')
matchStrs = perf_rs.get_match_triples(input)
print("\nPerforated sizes:")
print(matchStrs)
```

What this produces is much closer to what we expect:
```console
Imperforated:
[('imperf', 57, 63), ('imperforate', 92, 103), ('imperforate', 157, 168)]

Perforated sizes:
[('perf 15', 203, 210)]
```

### RegexString: build_regex_string( )

Now for some new RegexString functionality. First we'll use the function build_regex_string( ) to create a regular expression that matches on one set of list items on one word, then on another set for the next word in the text--this seems right for colors that are preceded by qualifiers like *bright* and *dark*.

Before going further let's have a look at the use of colors in the stamp descriptions--one description doesn't mention a color, one has just "black," and five have a *qualifier + color* description. The specific strings we're targeting are: dull red, black, red brown, bright blue, orange brown, dark green.

Now let's get started.

```python
colors = ['black', 'blue', 'brown', 'green', 'orange', 'red']

colors_rs = RegexString(colors, whole_word=True)
matchStrs = colors_rs.get_match_triples(input)
print("\nColors alone:")
print(matchStrs)

# Create the qualifiers.
# Add colors to the qualifiers, so that we can ID, e.g. 'orange brown'.
color_qualifiers = ['bright', 'dark', 'dull'] + colors

inputList = [color_qualifiers, 0, colors]
color_phrase_rs = RegexString.build_regex_string(inputList)
matchStrs = color_phrase_rs.get_match_triples(input)
print("\nColor qualifiers + colors:")
print(matchStrs)
```

Output:
```console
Colors alone:
[('red', 43, 46), ('black', 105, 110), ('red', 138, 141), ('brown', 142, 147), ('blue', 244, 248), ('orange', 276, 282), ('brown', 283, 288), ('green', 324, 329)]

Color qualifiers + colors:
[('dull red', 38, 46), ('red brown', 138, 147), ('bright blue', 237, 248), ('orange brown', 276, 288), ('dark green', 319, 329)]
```

Oops! We're not getting the colors which aren't preceded by a qualifier. The build_regex_string( ) function may be useful in other circumstances, but it's not the right tool for this particular job. (In truth, I knew this function wouldn't work here before I tried it out, but I wanted to introduce you to the function and I had no other use case for this set of postage stamp descriptions.)

Instead, let's try concat_with_word_distances( ), which we've already used successfully to identify *type + roman numeral*, a context where the first word was not optional.

```python
color_qualifiers_rs = RegexString(color_qualifiers, 
                                  whole_word=True, 
                                  optional=True
                                )
color_phrase_rs = RegexString.concat_with_word_distances(color_qualifiers_rs, 
                                                        colors_rs,
                                                        min_nbr_words=0, 
                                                        max_nbr_words=0)
matchStrs = color_phrase_rs.get_match_triples(input)
print("\nOptional color qualifiers + colors found in the input:")
print(matchStrs)
```

Final output:
```console
Optional color qualifiers + colors found in the input:
[('dull red', 38, 46), ('black', 105, 110), ('red brown', 138, 147), ('bright blue', 237, 248), ('orange brown', 276, 288), ('dark green', 319, 329)]
```

### RegexString: appending more complicated regular expressions

For our final example we're going to extract the Mystic Stamp Company's IDs for the postage stamps in our description. These are: # 11A, # 17, # 12, # 18, # 40, # 42, # 62B.

Our quick first pass uses RegexString with the `append` parameter, which completes the regular expression by matching on an empty space followed by one or more digits.

```python
id_symbols = ['#']

id_rs = RegexString(id_symbols, append='\s\d+')
matchStrs = id_rs.get_match_triples(input)
print("\nStamp IDs:")
print(matchStrs)
```

We see that this  gets the digit part of the IDs, but not the capital letter which follows two of them.

```console
Stamp IDs:
[('# 11', 0, 4), ('# 17', 65, 69), ('# 12', 112, 116), ('# 18', 170, 174), ('# 40', 212, 216), ('# 42', 250, 254), ('# 62', 290, 294)]
```

No problem. With our limited understanding of regular expressions, we know that we can add *(\w)?* to the end of the regular expression in order to match on an optional word character. (A word character excludes digits and punctuation.)
- If we use *\w+* instead of just *\w*, we could match on additional word characters, in case some of the IDs which we haven't seen have these extra characters. 
- And from the talk above regarding non-grouping expressions, we have learned that, generally speaking, we should insert *?:* at the start of the optional word character parentheses.

```bash
id_rs = RegexString(id_symbols, append='\s\d+(?:\w+)?')
matchStrs = id_rs.get_match_triples(input)
print("\nStamp IDs with letters found in the input:")
print(matchStrs)
```

```console
Stamp IDs with letters found in the input:
[('# 11A', 0, 5), ('# 17', 65, 69), ('# 12', 112, 116), ('# 18', 170, 174), ('# 40', 212, 216), ('# 42', 250, 254), ('# 62B', 290, 295)]
```

### Relation Extraction

By *relation extraction* we mean the identification of relationships between multiple entities. So, to use our postage stamp exercise as an example, creating a StampDescription class with properties such as *type*, *value* and *perforation_info* would qualify as relation extraction.

I have not done that, however. What I have done--and what I can offer as an example of relation extraction--is `relation_extraction/extract_min_max_relation.py`. You can find it in the source code at [the GitHub Text-to-Relations project](https://github.com/jkurlandski01/text_to_relations).

The Python code there takes you all the way from using RegexString to extract entities to subclassing the ExtractionPhaseABC abstract base class in order to combine those entities into a MinMax object based on text snippets like:
- *within the range of 60 to 90 points*
- *between 170 and 220 pounds*.
- *30 to 40 drinks*

The process begins by using RegexString to identify these entities:
- Number (for integers)
- Unit_of_Measure on the words *points*, *pounds* and *drinks*.

The process then passes these entities (as objects of the Text-to-Relations *Annotation* class) to two phases.
- Phase 1 creates a new temporary annotation called RangeMarker on phrases like *within the range of* and *between*. Then it looks for a **RangeMarker + Number + Number + Unit_of_Measure** in close proximity. If any are found, it creates a new MinMax annotation.
- Phase 2 creates a new temporary annotation called ToMarker on *to* and *-* (the hyphen character). Then it looks for a **Number + ToMarker + Number + Unit_of_Measure** in close proximity. If any are found, it creates a new MinMax annotation.

There is a critical snippet of code which is executed after Phase 1 and before Phase 2. You can find this in the run_extraction_phases( ) function of `extract_min_max_relation.py`. It is designed to prevent Phase 2 from matching on any of the Number and Unit_of_Measure entities which were used to create MinMax relations in Phase 1, and it accomplishes this by removing from the annotation list all Number and Unit_of_Measure annotations which are enclosed by the MinMax relations extracted in that phase.

**SentenceAnn**: There is a class called SentenceAnn which subclasses Annotation. Not used in the MinMax extraction discussed here, it could be useful (in combination with Annotation.encloses( )) if you wanted to require that relations occur within a single sentence. Naturally, to succeed here the Spacy sentence-splitting, which is used here, must be correct.
