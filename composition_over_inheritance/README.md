
#### Composition over inheritance rule
- This grand principle encourages software architects to escape from **object orientation** and follow the simpler practices of **object based programming**.

#### Subclass Explosion Problem
- A crucial weakness of inheritance as a design strategy is that a class often needs to be specialized along several different design axes at once, leading to **proliferation of classes**.

#### Order of reading codes in files
- logging_explosion.py
- beyond_gof.py
- dodge_if_statements.py
- dodge_multiple_inheritance.py
- dodge_mixins.py
- dodge_building_classes_dynamically.py


#### Drawbacks of using multiple if statements
- Locality:- If we are tasked with improving or debugging one particular feature — say, the support for writing to a socket — we will find that we can’t read its code all in one place. The code behind that single feature is scattered between the initializer’s parameter list, the initializer’s code, and the log() method itself.
- Deletability:- An underappreciated property of good design is that it makes deleting features easy. In the case of our class-based solutions, we can trivially delete a feature like logging to a socket by removing the SocketHandler class and its unit tests once the application no longer needs it. By contrast, deleting the socket feature from the forest of if statements not only requires caution to avoid breaking adjacent code, but raises the awkward question of what to do with the socket parameter in the initializer.
- Dead code analysis:- dead code analyzers can trivially detect when the last use of SocketHandler in the codebase disappears. But dead code analysis is often helpless to make a determination like “we can now remove all the attributes and if statements related to socket output, because no surviving call to the initializer passes anything for socket other than None.”
- Testing:- One of the strongest signals about code health that our tests provide is how many lines of irrelevant code have to run before reaching the line under test. But testing socket logging in our forest of if statements will run at least three times the number of lines of code.
- Efficiency:- But the design problems with the forest of if statements are also signalled by the approach’s inefficiency. Even if you want a simple unfiltered log to a single file, every single message will be forced to run an if statement against every possible feature you could have enabled. The technique of composition, by contrast, only runs code for the features you’ve composed together.

#### Drawbacks of using multiple inheritance
- Introspection is difficult - can only learn which filter and logger have been combined by examining the metadata of the class itself — either by reading its __mro__ or subjecting the object to a series of isinstance() tests.
- Changing an object’s class at runtime is not impossible in a dynamic language like Python, it’s generally considered a symptom that software design has gone wrong.
- Finally, multiple inheritance provides no built-in mechanism to help the programmer order the base classes correctly. The FilteredSocketLogger won’t successfully write to a socket if its base classes are swapped.

#### Drabacks of mixins
- FilterMixin only needs tests that combine it with a logger. Because the mixin is by itself incomplete, a test can’t even be written that runs it standalone.
- But all the other liabilities of multiple inheritance still apply. So while the mixin pattern does improve the readability and conceptual simplicity of multiple inheritance, it’s not a complete solution for its problems.


#### Drawbacks of building class dynamically
- Readability Suffers
- Debugging becomes more difficult as class of the name does not exist.
- Type introspection will fail
- Matplotlib builds at runtime, through type()
