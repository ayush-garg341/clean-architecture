#### Inheritance ( exmaples in python )

- Inheritance models what’s called an **is a** relationship.
- Classes that inherits from other classes are called Derived classes, subclasses or subtypes.
- Classes from which other classes are derived are called base classes or super classes.
- A derive class is said to derive, inherit or extend a base class.

#### Overview
- Everything in Python is an object. Modules are objects, class definitions and functions are objects, and of course, objects created from classes are objects too.
- Object super class
    ```
    o = object()
    dir(o)

    class Empty():
        pass
    c = Empty()
    dir(c)
    ```
- Every class inherits from object super class but with an exception of Exceptions.
    ```
    class NotAnError():
        pass

    raise NotAnError()
    ```
- In the above example, we will get a TypeError saying that Exception classes must inherit from **BaseException** class. Below is a fix for it.
    ```
    class AnError(Exception):
        pass

    raise AnError()
    ```

- Implementation inheritance vs Interface inheritance
    - When we derive one class from another, the derived class inherits both of the following:-
        - The base class interface:- The derived class inherits all the methods, properties, and attributes of the base class.
        - The base class implementation:- The derived class inherits the code that implements the class interface.

- In Python, we don’t implement interfaces explicitly. Any object that implements the desired interface can be used in place of another object. This is known as **duck typing**.
    ```
    class SpecialEmployee:
        def __init__(self, id, name):
            self.id = id
            self.name = name

        def calculate_payroll(self):
            return 1_000_000

    # PayrollSystem can process this class object because it meets the desired interface.
    ```

- Since we don’t have to derive from a specific class for our objects to be reusable by the program, we may be asking why we should use inheritance instead of just implementing the desired interface.
    - Use inheritance to reuse an implementation:- derived classes should leverage most of their base class implementation. They must also model an is a relationship.
    - Implement an interface to be reused:- When we want our class to be reused by a specific part of our application, we implement the required interface in our class, but we don’t need to provide a base class, or inherit from another class.

#### Class Explosion Problem
- Inheritance can lead to a huge hierarchical class structure that’s hard to understand and maintain.
- Now let's say we need to add functionality to our PayrollSystem based on productivity of employees i.e ProductivitySystem.

#### Multiple Inheritance
- Ability to derive a class from multiple base classes at the same time.
- Usecase:- It turns out that sometimes temporary secretaries are hired when there’s too much paperwork to do.
            - The TemporarySecretary class performs the role of a Secretary in the context of the ProductivitySystem, but for payroll purposes, it’s an HourlyEmployee
