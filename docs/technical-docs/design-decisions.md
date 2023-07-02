---
title: Design Decisions
parent: Technical Docs
nav_order: 5
---

Michael Otieno
{: .label .label-red }
Justin Grünberg
{: .label .label-green }
Linus Widing
{: .label }

# Design decisions
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>



Linus Widing
{: .label }
## 01: Choosing the Right Tool for Database Access: SQL or SQLAlchemy

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 05-05-2023

### Problem statement

Figure out, which tool to use for accessing and maintaining the database.
Options: 
1. plain SQL
2. SQLAlchemy

With plain SQL we would have to write queries, ddl and dml statements manually.\
With SQLAlchemy we would take advantage of object relational mapping to map the database to python
classes. Querying is done via the SQLAlchemy framework.

### Decision

Linus made the decision, that SQLAlchemy is the better choice. In the past we worked with plain SQL and wanted to try something new.
Research has shown, that it is very easy to connect SQLAlchemy to Flask, wich is the framework for our Backend.
Also, we are most likely going to change the database schema a lot, wich is less work to do in SQLAlchemy.

### Regarded options

|      | plain SQL                           | SQLAlchemy                                                               |
|------|-------------------------------------|--------------------------------------------------------------------------|
| Pros | - we already know what we are doing | - less code<br/>- querying is much easier<br/>- easy to connect to flask |
| Cons | - a lot of boilerplate code         | - we need to learn how to use SQLAlchemy                                 |

---



Justin Grünberg
{: .label .label-green }
## 02: Choosing Between Bootstrap and Custom CSS for website design

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 07-05-2023

### Problem statement

Should we craft our web designs from scratch using CSS, or harness the efficiency and speed afforded by using Bootstrap?

### Decision

We have chosen Bootstrap for our app's design due to its vast array of customizable templates which facilitate a more efficient development process. Our prior experience with CSS allows us to focus on enhancing the app's functionality, as Bootstrap saves us the time we would otherwise spend crafting designs from scratch. This strategic decision allows us to prioritize our app's user experience and operational effectiveness.


### Regarded options

|      | Bootstrap               | CSS from Scratch     |
|------|-------------------------|----------------------|
| Pros | - efficiency and Speed  | - full Customization |
| Cons | - limited Customization | - time-Consuming     |

---



Michael Otieno
{: .label .label-red }
## 03: Way of implementing forms

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 07-06-2023

### Problem statement

How to receive and process user-input

options:

1. WTForms

2. html-forms

HTML forms and WTForms are both tools used for handling form submissions in web applications, but they serve different purposes and have distinct advantages.

### Decision

Michael decided to make use of html-forms. Main reason being its simplicity. Html-forms provides
a straightforward way to create and handle submissions without relying on external libraries and frameworks

### Regarded options

|      | WTForms                                                                                                 | HTML Forms                                                                             |
|------|---------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| Pros | - simplification for defining and validating forms using Python classes.<br/>- Built-in form validation | - Simple and flexible<br/>- Customizable using CSS and JavaScript                      |
| Cons | - Learning curve                                                                                        | - No built-in abstraction or validation<br/>- Requires more manual handling and coding |

---



Linus Widing
{: .label }
## 04: Homepage with infinite scroll or pagination

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 10-07-2023

### Problem statement

The purpose of our homepage is to find the right recipe. Therefore, it should be possible to view a lot of 
recipes to find the right one. 

### Decision

We will use an infinite scroll. Our app should be in a social media style, therefore an infinite scroll
better to constantly server new recipes.

### Regarded options

---

