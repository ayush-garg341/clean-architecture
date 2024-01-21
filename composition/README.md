#### Composition
- Models has-a relationship.
- Class known as **composite** contains an object or component of another class.
- Composition is more flexible than inheritance because it models a loosely coupled relationship.

#### Order of reading code
- address.py
- employees.py
- productivity.py
- payroll_system.py
- program.py

#### Changing behaviour
- If design relies on Inheritance, then need to find a way to change the type of an object to change its behavior.
- With composition, just need to change the policy that the object uses.
    ```
    employees = employee_database.employees
    manager = employees[0]
    manager.payroll = HourlyPolicy(55)
    ```

#### Choosing between inheritance vs composition
- The general advice is to use the relationship that creates fewer dependencies between two classes. This relation is composition.
- Inheritance:
    - Use inheritance to model an is a relationship.
    - Liskov’s substitution principle is the most important guideline to determine if inheritance is the appropriate design solution.
    - Liskov’s substitution principle says that an object of type Derived, which inherits from Base, can replace an object of type Base without altering the desirable properties of a program.
    - Let's say we have two classes A and B. A, provides an implementation and interface you want to reuse in another class, B. Initial thought is that we can derive B from A and inherit both the interface and the implementation. To be sure this is the right design, follow these steps:
        - B is an A
        - A is a B
    - If we can justify both relationships, then we should never inherit those classes from one another.

    - Mixins ( mixin.py )
        - A mixin is a class that provides methods to other classes but isn’t considered a base class.
        - One of the uses of multiple inheritance in Python is to extend class features through mixins.
        - A mixin allows other classes to reuse its interface and implementation without becoming a superclass.
- Composition
    - Provides a loosely coupled relationship that enables flexible designs and can be used to change behavior at runtime.

