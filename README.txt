========================================================================================================
  This file will serve as my personal notes while working on the project
  Its my reasoning and talking to myself as I work on the problem
  Done in order to have a better idea of exactly what happened for when Im writing the real report
  Git version history should keep track of all changes
========================================================================================================

Alright so, recap
  
  The core of the problem is that I dont want internet data brokers to be able to track me through every single site i go whether i like it or not
  They do this via injecting a fingerprinting script into the site
    sometimes this is done intentionally by the site itself
      maybe to track malicious users or keep state rather than using cookies etc
    often times this is done by third parties that just want all your information
      if you use a facebook asset in your site, when the browser fetches the asset it needs to visit facebook servers, where they can fingerprint you and keep track of where you came from, who you are etc
        this means that if the site is large enough(big social media sites/hosting providers etc) then it can realistically track you across a very large portion of the internet without any help of the sites you are actually visiting

  The fingerprinting script will use browser API's as well as javascript scripts in order to gather information about your system
    Browser API will give you information like user agent, referer, Underlying operating system etc etc
    scripts are used to have your system run many operations/calculations that produce a somewhat unique value, or a set of them
      this could be having your system calculate some form of audio wave, and then hashing the value that it returns to the script after completion
        this is a fingerprintable value as it is somewhat unique since it needs to pass through a chain of audio nodes which vary system to system
      Floating point operations are also used as different processors and system configurations can result in slightly varying results
          
          example object of maths based fingerprinting from my browser

          "math": {
            "value": {
              "acos": 1.4473588658278522,
                "acosh": 709.889355822726,
                "acoshPf": 355.291251501643,
                "asin": 0.12343746096704435,
                "asinh": 0.881373587019543,
                "asinhPf": 0.8813735870195429,
                "atanh": 0.5493061443340548,
                "atanhPf": 0.5493061443340548,
                "atan": 0.4636476090008061,
                "sin": 0.8178819121159085,
                "sinh": 1.1752011936438014,
                "sinhPf": 2.534342107873324,
                "cos": -0.8390715290095377,
                "cosh": 1.5430806348152437,
                "coshPf": 1.5430806348152437,
                "tan": -1.4214488238747245,
                "tanh": 0.7615941559557649,
                "tanhPf": 0.7615941559557649,
                "exp": 2.718281828459045,
                "expm1": 1.718281828459045,
                "expm1Pf": 1.718281828459045,
                "log1p": 2.3978952727983707,
                "log1pPf": 2.3978952727983707,
                "powPI": 1.9275814160560206e-50
            },
              "duration": 0
          },

  Many anti fingerprinting tools will try to block or spoof these attributes
    the problem is doing this incorrectly actually makes you stand out more, as most people will not be doing this
      FP-Block paper calls this the 'defensive paradox'
        if you block a commonly unblocked attribute, it may make you unique enough that the rest of the results from the fingerprinter are enough to identify you regardless

    A similar issue exists with spoofing
      if you claim to have a system configuration that logically doesnt make any sense, no legitimate users will have the same configuration/fingerprint as you, again making you stand out more
          this could be an iphone2 claiming to have a recently released javascript runtime engine etc.


  This means that you need to have logically sound, legitimate fingerprint values in order for it to make any sense and not stand out further
    This means that the resulting fingerprint can be modelled as a markov chain
        stole this from the FP-Block paper

      basically you need to work your way up to a full fingerprint instead of just picking parts out of a hat
      i.e. start with OS and CPU, then pick kernel version based off of those, then pick browser and user agent based off of those etc etc etc until you have a full 'real' looking system
      
  Following that approach should lead you to having a different fingerprint to your original one, while still fitting in with the surrounding ones of real people
      this is the key bit that makes it work


  Now the second part of this involves being tracked across sites
    in reality i dont care if a site recognises me, i care if i am recognised across sites
    this is where FP-Blocks web identity comes in

    Generating a different fingerprint for each site you visit, and the sites you visit FROM that site, makes the fingerprinter think that you are a different person each time it sees you

    1.
              /---- site2
    site1 ---
              \----  site3 --- site4

    2.
    site2 --- site4


    in the bad diagram above, fig 1 shows you visiting site1, then getting redirected to site 2,3 and 4
    sites 2,3,4 will see the fingerprint corresponding to site1

    in fig 2, you start visiting site2, meaning that you have a separate fingerprint for site 2 that your browser 'adopts'
    if you then visit site4 through site2, it will see the fingerprint corresponding to site2

  This means that site4 will think you are 2 separate users, assuming that the identities are sufficiently different and logically sound
  


There is already a re-implementation of the FP-Block approach, so i dont reeeealy want to just remake a project someone else has already made


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
  turns out actually really easy


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



Okay whatever lets just get started
Need the data first of all
Regardless, in order to plot anything on a graph i need to convert the fingerprint JSON object into a numerical vectorised representation
  for now im just gonna make vectorizer.py and then see where we go


Forget using VM's, im fingerprinting through the browser and its so much harder to automate VMs than docker containers
  chances are its not going to get full system information






