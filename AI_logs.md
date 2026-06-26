# AI Collaboration Log

## Project

**Website Uptime Monitoring Dashboard**

This project was developed through iterative collaboration with AI rather than generating the entire application in a single prompt. My approach was to use AI as an engineering partner—breaking the problem into smaller components, reviewing the generated solution, and making architectural decisions before moving on to the next module.

---

# AI Tech Stack

| Tool              | Purpose                                                                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ChatGPT (GPT-5.5) | System design discussions, backend implementation, SQL schema design, scheduler architecture, frontend generation, debugging and code reviews |

---

# Development Workflow

Instead of prompting AI to "build the entire application", I intentionally developed the project incrementally.

The implementation order was:

1. PostgreSQL schema design
2. FastAPI project structure
3. Database connection layer
4. Helper utilities
5. CRUD layer
6. Scheduler implementation
7. FastAPI routes
8. Dashboard UI
9. Live frontend updates
10. Filtering functionality

This allowed every module to be tested before proceeding to the next.

---

# Prompts That Shipped The Project

Below are representative prompts that directly contributed to the final implementation.

## 1. Database Design

> "I'm building a Uptime Monitoring System for webURLs. I'm setting up the Database for it. The DB will have 2 tables... Write the SQL Query to create the above tables. SQL queries should be PostgreSQL compliant."

This established the initial schema for:

* website_listing
* website_tracking

Later, the schema evolved to replace SERIAL WebIDs with custom IDs (`WEB_01`, `WEB_02`, ...), and a `response_difference` column was introduced based on implementation needs.

---

## 2. Frontend Dashboard

> "Frontend: The header of the page will have 'Uptime Monitoring'... Use HTML, CSS & Bootstrap for frontend. Keep the html & css in different files."

This produced the initial dashboard layout consisting of:

* Website registration form
* Tracking status table
* Bootstrap styling

---

## 3. Backend Integration

> "The FastAPI will directly land on the dashboard. No Separate pages... create a helper function that will generate primary key for every new website."

This drove the implementation of:

* Jinja2 integration
* Custom WebID generation
* FastAPI routes
* Database insertion flow

---

## 4. Scheduler Architecture

During implementation, I questioned whether each website should have its own trigger.

After discussing scalability, I decided to replace the trigger-based design with a single scheduler responsible for monitoring all websites.

Prompt:

> "Okay, so let's drop the idea of scheduler in the background. Scheduler running only when FastAPI is good with the Goal of creating a MVP."

This resulted in:

* One monitoring thread
* Polling every minute
* Automatic monitoring for all tracked websites

---

## 5. Live Dashboard Updates

The original dashboard required manual refreshes.

I requested:

> "The tracking status table should get updated after every minute. I don't have to refresh the page again and again every minute."

The implementation was changed to:

* AJAX endpoint (`/tracking-data`)
* JavaScript Fetch API
* Automatic table refresh
* No full page reload

---

## 6. Filtering Support

To improve usability I requested:

> "I want to add one more function. Filtering option. From filter tab, user can select which named website he wants..."

This introduced:

* Website filter dropdown
* Dynamic API queries
* Backend filtering
* Live filtered updates

---

# Course Corrections

Several implementation decisions changed during development after evaluating AI suggestions.

## 1. Scheduler Architecture

### Initial idea

Create a separate trigger or background task for every newly added website.

### Issue

This would create one long-running task per website, making the design unnecessarily complex and difficult to scale.

### Final decision

Replace individual triggers with a single scheduler that:

* Runs every minute
* Reads all active websites from the database
* Monitors each website sequentially
* Stores tracking records

This significantly simplified the architecture.

---

## 2. Response Difference Calculation

Initially, the response difference was planned inside the helper responsible for sending HTTP requests.

After reviewing responsibilities, I moved the calculation into the scheduler because it already had access to previous tracking records from the database.

Formula used:

Current Response Time − Previous Response Time

This separated HTTP logic from database logic.

---

## 3. Live Dashboard Rendering

The first implementation rendered tracking data entirely using Jinja templates.

This required manually refreshing the page.

The implementation was later redesigned to expose a JSON API (`/tracking-data`) and update only the table using JavaScript, resulting in a much smoother user experience.

---

# What AI Was Used For

AI was primarily used for:

* SQL query generation
* FastAPI boilerplate
* HTML/CSS generation
* Refactoring suggestions
* API design
* Scheduler implementation
* Code reviews
* Architectural discussions

---

# Human Decisions

The following design decisions were intentionally made during development rather than being accepted blindly from AI:

* Choosing a scheduler instead of one trigger per website.
* Switching from page refreshes to asynchronous table updates.
* Using custom WebIDs (`WEB_01`) instead of database-generated IDs.
* Keeping monitoring logic separate from CRUD operations.
* Filtering records by immutable `web_id` instead of website name.
* Breaking the project into modular components instead of generating the application in a single step.

---

# Reflection

The project was built through iterative collaboration with AI rather than code generation alone. AI accelerated implementation of individual modules, while architectural choices, refinement, integration, and feature evolution were guided through multiple review-and-revision cycles until the final design met the project requirements.
