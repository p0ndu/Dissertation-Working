========================================================================================================
  This file will serve as my personal notes while working on the project
  Its my reasoning and talking to myself as I work on the problem
  Done in order to have a better idea of exactly what happened for when Im writing the real report
  Git version history should keep track of all changes
========================================================================================================

########################################################################################################
        Plan

First need to setup a way to fingerprint myself
  some kind of webserver on localhost that just has a homepage and fingerprintjs running on it
    Just use the stuff I know
      or better find one of my old projects and throw up the code, like the fullstack one


  setup and run fingerprintjs on the webserver

  visit it on chrome and see what i get



fingerprintjs
  says it wont work using an import if visitor is running firefox or a blocker

Web server is running
  Im getting a different fingerprint value on zen vs chromium

  why could this be?

    Different User agent
      check the outbound requests
    
    Maybe one of them is spoofing or blocking something
      check zen for this

    free one is meant to be much worse so it could just not be as good

Displaying the get request from each browser
  very different LMAO
  no wonder its not the same fingerprint

  turns out zen is built off of firefox not chrome, which is why the headers are as different as they are


What else I want to do
  Visit it in kali
    one with the same browser one with a different one
    should probably batch test different operating systems tbh
  find a way to display the fingerprint object and see the attributes rather than just the ID
  maybe get another chromium browser and see if it would fingerprint the same thing


I want to see if i can get the attributes that it finds rather than just the raw fingerprint result


Seems like I need to use Vagrant to manage virtual box machines
  Vagrant boots and kills machines, then runs a script on startup
   - Get lots of different linux distros and one for windows
   - have them boot
   - connect to my local webserver
   - get fingerprinted
   - shutdown

  Webserver just needs to fingerprint and store each of the objects somewhere with some form of name


 
 What do I actually do with this data?
 I need a way to compare how much different changes affect the fingerprint
  I could base it off the values in the fingerprint object but is comparing entropy really the best way?
  
The paper compared the result of applying each fingerprinter to sample data but that doesnt really apply here

I want to know how much each change in value 'Shifts' my fingerprint
that means I need some way to graph all the fingerprints and then see how moving the attributes moves my position on the graph
  Get the test data from fingerprintme or amIUnique or whatever the site was

I guess its a good thing my other class is data science huh


How can I plot this graph when its such a variety of things being checked
  Could plot each attribute and how my changes vary it
  could plot the final fingerprint 'hash value'
    the like final number it gives you im assuming it is some kind of hash


