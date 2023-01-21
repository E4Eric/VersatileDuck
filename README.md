# VersatileDuck
A first principals approach to a UI Toolkit. The idea is to take a few existing 
UI's and attempt to mimic them in the simplest way possible.

## Caution ! This project is in early development !! Anything can change as I iterate....

# Running the demo
 - Have Python installed
 - install json if necessary ('pip install json')
 - Clone the repo into a new dir (I'll call it 'test')
 - Drill down to 'test\VersatileDuck\FPGui\PythonQt5Impl' (I'll clean this up later)
 - Run it !! 'python pythonDuck.py'

# What does 'First Principals' mean in the context ?

Essentially doing something from first principals has two features:
  - You know where your need to go beforehand
  - You believe that there may be a simpler way to get there

For this exercise where we're going is Desktop User Interfaces. The aim is to reproduce this type of application (both in look and operaton) using the simplest approach

In the case of User Interfaces there's good reason the expect that there is a simpler way to achieve the same result. UI development today is generally done using one of a bewildering array of toolkits (most containing the 'conventional' UI Widgets; Menus, Toolbars. etc). The use of the term 'conventional' here isn't accidental; these conventions were adopted over time and became so common that Users knew the terms. We're gonna use this to our advantage...;-).

# Informing the Architecture

A UI is:
  - An app that allows the user push their intent into the computer through a keyboard and a mouse; good ones assist the user
  - By its nature a UI's most important pixels are those the User is expected to interact with (think Tool / Menu Items...); everything else exists for style and put the important bits where they should be according to the conventions of the style of UI you want to 'duck'. 

First, let's go back to a time before we started the whole toolkit thing. What UI's existed were hand crafted. Our job category was 'Information Processing'....;-)

OK, we know what we're going so how can we leverage that?
  - UI's of this type are 'completely tiled' (cover the whole app surface without gaps)


Known Issues:
  Views are faked by hacking the style sheet to provide the contents
  Layout very good but not yet pixel perfect
To Run:

You'll need 
