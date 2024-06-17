FLOWCHART = """Convert the given text into UML code for a detailed Mermaid flowchart, ensuring it 
includes nodes, edges, node shapes (round edges, stadium, subroutine, cylindrical, circle, asymmetric, rhombus, 
hexagon, parallelogram, trapezoid), link styles (arrow heads, open links, text, dotted, thick, invisible), 
orientations (TB, TD, BT, RL, LR), special characters, subgraphs, markdown strings, interactions, and styling 
(links, nodes, CSS classes, Font Awesome icons). Focus on accurate syntax and feature representation from Mermaid 
flowchart guidelines. Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "flowchart LR
subgraph "One"
  a("`The **cat**
  in the hat`") -- "edge label" --> b{{"`The **dog** in the hog`"}}
end
subgraph "`**Two**`"
  c("`The **cat**
  in the hat`") -- "`Bold **edge label**`" --> d("The dog in the hog")
end"}
"""

SEQUENCE = """Create UML code for a detailed Mermaid sequence diagram based on the provided text. 
This diagram should visually represent the interaction between processes, detailing their order and nature of 
communication. Key features include defining participants or actors, their order of appearance, message types 
(solid or dotted lines), activations, notes, loops, alternatives, parallel actions, critical regions, breaks, 
and background highlights. Handle special considerations like enclosing 'end' in symbols if necessary. Incorporate 
comments and entity codes for character escape. Optionally, include actor menus and configure styles via CSS.
Ensure the diagram is clear, accurate, and follows the syntax and examples provided. 
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "sequenceDiagram
    participant A as Alice
    participant J as John
    A->>J: Hello John, how are you?
    J->>A: Great!"}
"""

CLASS = """Transform the following text description into a UML class diagram code suitable for 
Mermaid. The description includes classes with their names, attributes, operations, and 
relationships. Ensure that the classes are correctly defined, with their attributes and methods 
appropriately formatted according to UML conventions. Include relationships such as inheritance, 
composition, aggregation, association, and dependencies. Apply visibility symbols correctly for 
each class member. Consider the use of generics, labels, cardinality, annotations, and comments 
where necessary. The final code should accurately reflect the given text in a format that can be 
rendered by Mermaid to visualize the class diagram.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "classDiagram
    note "From Duck till Zebra"
    Animal <|-- Duck
    note for Duck "can fly\ncan swim\ncan dive\ncan help in debugging"
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
        +String beakColor
        +swim()
        +quack()
    }
    class Fish{
        -int sizeInFeet
        -canEat()
    }
    class Zebra{
        +bool is_wild
        +run()
    }"}"""

STATE = """Convert the following textual description into a state diagram code compatible with 
Mermaid syntax. The text outlines a system's states, transitions, and behaviors. Create code that
accurately represents states, including composite states and special states like start and end.
Include transitions with appropriate annotations, and implement elements like choices, forks, 
and concurrency where applicable. Ensure the code reflects the given description's logic and 
hierarchy, adhering to the syntax for Mermaid's state diagrams, including notes and optional 
styling using classDefs. The resulting code should enable a clear and precise visualization of 
the state diagram as described in the text.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "stateDiagram-v2
    [*] --> Still
    Still --> [*]

    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]"}"""

ERDIAGRAM = """Transform the provided text information into an Entity Relationship (ER) diagram code 
suitable for rendering in Mermaid. Ensure that the code accurately represents the entities, 
their attributes, and the relationships among them, as described in the text. Include entity
names (preferably capitalized for clarity), attribute definitions (with type and name), and 
relationship connections using Mermaid's crow's foot notation. Pay attention to relationship 
types, whether identifying or non-identifying, as well as cardinality aspects (one-to-one, one-to-many, etc.).
Incorporate relationship labels appropriately to describe the interactions from the perspective 
of the first entity. Optionally, consider the inclusion of foreign keys in attribute lists if 
relevant to the diagram's purpose. The resulting code should visually articulate the ER model's 
structure and relationships as outlined in the provided text, aligning with Mermaid's syntax for 
ER diagrams.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "erDiagram
    CUSTOMER }|..|{ DELIVERY-ADDRESS : has
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER ||--o{ INVOICE : "liable for"
    DELIVERY-ADDRESS ||--o{ ORDER : receives
    INVOICE ||--|{ ORDER : covers
    ORDER ||--|{ ORDER-ITEM : includes
    PRODUCT-CATEGORY ||--|{ PRODUCT : contains
    PRODUCT ||--o{ ORDER-ITEM : "ordered in""}"""

JOURNEY = """Create a User Journey diagram code for Mermaid using the provided text details. 
Structure the code to reflect the various stages of a user's interaction with a system, 
application, or website. Divide the journey into distinct sections, each representing a part 
of the task the user is completing. For each task within these sections, include the task name, 
a score rating (to indicate the task's ease, difficulty, or priority), and the actors involved 
(e.g., users or system components). Ensure that the code captures the entire flow of the user's 
experience as described, highlighting key interactions and transitions from one task to another.
The final code should present a clear and structured overview of the user's journey, suitable for
rendering in Mermaid format.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "journey
    title My working day
    section Go to work
      Make tea: 5: Me
      Go upstairs: 3: Me
      Do work: 1: Me, Cat
    section Go home
      Go downstairs: 5: Me
      Sit down: 5: Me"}"""

GANTT = """Create a Gantt diagram code using Mermaid syntax based on the provided text details.
Structure the code to reflect the project schedule, including tasks, their start dates, durations,
and dependencies. Define each task clearly with a unique identifier, and specify the relationships 
between tasks, such as sequential or concurrent tasks. Include any milestones, excluded dates, or 
non-working days as necessary. Adjust the formatting to suit the project timeline, using the 
appropriate date formats and axis labels. The final code should visually represent the project's 
timeline, capturing key tasks, durations, and dependencies, suitable for rendering in Mermaid format.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "gantt
    title A Gantt Diagram
    dateFormat YYYY-MM-DD
    section Section
        A task          :a1, 2014-01-01, 30d
        Another task    :after a1, 20d
    section Another
        Task in Another :2014-01-12, 12d
        another task    :24d"}"""

PIE = """Create a Pie Chart diagram code using Mermaid syntax based on the provided textual data.
Start with the pie keyword, optionally include the showData keyword if you want to display the 
actual data values next to the legend. If a title is necessary, use the title keyword followed 
by the desired title for the pie chart. For each data set, provide a label for the section 
enclosed in quotes, followed by a colon, and then the numeric value representing that slice of 
the pie. Ensure that the pie slices are proportionally represented according to the provided 
data values. The final code should visually depict the numerical proportions of different 
categories in a pie chart format, suitable for rendering in Mermaid.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "pie title Pets adopted by volunteers
    "Dogs" : 386
    "Cats" : 85
    "Rats" : 15"}"""

QUADRANT = """Construct a Quadrant Chart diagram using Mermaid syntax based on the provided textual
information. Begin with the quadrantChart keyword. If needed, include a title for the chart.
Define the x-axis and y-axis labels to represent the two variables of your data set. For each 
quadrant, provide a description that captures the essence of the data points falling into that
quadrant. Plot the data points on the chart by specifying their x and y coordinates, ranging 
from 0 to 1, where each point represents a unique data item. Optionally, adjust the chart 
configurations like chart dimensions, padding, text sizes, and theme variables for custom styling.
The final code should visually represent the data in a two-dimensional grid, dividing it into 
four quadrants to highlight patterns, trends, or priorities as indicated by the data points' positions.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "quadrantChart
    title Reach and engagement of campaigns
    x-axis Low Reach --> High Reach
    y-axis Low Engagement --> High Engagement
    quadrant-1 We should expand
    quadrant-2 Need to promote
    quadrant-3 Re-evaluate
    quadrant-4 May be improved
    Campaign A: [0.3, 0.6]
    Campaign B: [0.45, 0.23]
    Campaign C: [0.57, 0.69]
    Campaign D: [0.78, 0.34]
    Campaign E: [0.40, 0.34]
    Campaign F: [0.35, 0.78]"}"""

REQUIREMENT = """"Develop a Requirement Diagram using Mermaid syntax to visualize the relationships 
between various requirements and elements as specified in the text. Start with the 
requirementDiagram keyword. Define each requirement and element with their respective attributes 
such as id, text (no `-`), risk, verifymethod, type, and docRef. Utilize the appropriate
keywords for requirement types (like requirement, functionalRequirement, etc.) and relationship 
types (such as satisfies, traces, contains). Ensure that the relationships accurately connect the 
requirements and elements as described. The final code should clearly represent the structure of 
requirements, their interdependencies, and connections to other documented elements, adhering to 
the SysML v1.6 specification for requirement modeling.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

<type>: requirement, functionalRequirement, interfaceRequirement, performanceRequirement, physicalRequirement, designConstraint
<risk>: low, medium, high
<verifymethod>: analysis, inspection, test, demonstration
<text>: Only alphabets and numbers. Do not use `-`

Example: {"code": "requirementDiagram

    requirement test_req {
    id: 1
    text: the test text. 
    risk: high
    verifymethod: test
    }

    element test_entity {
    type: simulation
    }

    test_entity - satisfies -> test_req"}"""

GITGRAPH = """Construct a Gitgraph diagram using Mermaid syntax to depict the git commits and 
actions on various branches as specified in the text. Start with the gitGraph keyword, followed 
by a sequence of git operations such as commits, branch creations, checkouts, and merges.
Use the commit keyword to represent new commits on the current branch, branch to create and 
switch to a new branch, checkout to switch to an existing branch, and merge to merge one branch 
into another. Optionally, include custom commit ids, tags, types (like HIGHLIGHT or REVERSE), 
and cherry-picking of commits from other branches. Ensure that the diagram accurately represents 
the git history and branch management strategy described in the text, including the branching, 
merging, and commit patterns. The final code should offer a clear visual representation of the 
git operations and branch interactions, suitable for rendering in Mermaid format
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "gitGraph
   commit
   commit
   branch develop
   checkout develop
   commit
   commit
   checkout main
   merge develop
   commit
   commit"}"""

C4DIAGRAM = """Design a comprehensive C4 Diagram using Mermaid's syntax to visually represent the 
architecture of a software system. The diagram should include various elements such as System, 
Container, Component, Person, and System_Ext to illustrate the different parts of the system and 
their interactions. Utilize the appropriate C4 model type, whether it's a System Context 
(C4Context), Container diagram (C4Container), Component diagram (C4Component), Dynamic diagram 
(C4Dynamic), or Deployment diagram (C4Deployment). Detail each element with labels, descriptions, 
and connections, ensuring to represent the relationships accurately with Rel or BiRel commands.
Adjust the appearance and layout of the diagram using UpdateElementStyle, UpdateRelStyle, and 
UpdateLayoutConfig commands. The final diagram should offer a clear and structured visualization 
of the system architecture, suitable for understanding by both technical and non-technical stakeholders.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "C4Context
      title System Context diagram for Internet Banking System
      Enterprise_Boundary(b0, "BankBoundary0") {
        Person(customerA, "Banking Customer A", "A customer of the bank, with personal bank accounts.")
        Person(customerB, "Banking Customer B")
        Person_Ext(customerC, "Banking Customer C", "desc")

        Person(customerD, "Banking Customer D", "A customer of the bank, <br/> with personal bank accounts.")

        System(SystemAA, "Internet Banking System", "Allows customers to view information about their bank accounts, and make payments.")

        Enterprise_Boundary(b1, "BankBoundary") {

          SystemDb_Ext(SystemE, "Mainframe Banking System", "Stores all of the core banking information about customers, accounts, transactions, etc.")

          System_Boundary(b2, "BankBoundary2") {
            System(SystemA, "Banking System A")
            System(SystemB, "Banking System B", "A system of the bank, with personal bank accounts. next line.")
          }

          System_Ext(SystemC, "E-mail system", "The internal Microsoft Exchange e-mail system.")
          SystemDb(SystemD, "Banking System D Database", "A system of the bank, with personal bank accounts.")

          Boundary(b3, "BankBoundary3", "boundary") {
            SystemQueue(SystemF, "Banking System F Queue", "A system of the bank.")
            SystemQueue_Ext(SystemG, "Banking System G Queue", "A system of the bank, with personal bank accounts.")
          }
        }
      }

      BiRel(customerA, SystemAA, "Uses")
      BiRel(SystemAA, SystemE, "Uses")
      Rel(SystemAA, SystemC, "Sends e-mails", "SMTP")
      Rel(SystemC, customerA, "Sends e-mails to")

      UpdateElementStyle(customerA, $fontColor="red", $bgColor="grey", $borderColor="red")
      UpdateRelStyle(customerA, SystemAA, $textColor="blue", $lineColor="blue", $offsetX="5")
      UpdateRelStyle(SystemAA, SystemE, $textColor="blue", $lineColor="blue", $offsetY="-10")
      UpdateRelStyle(SystemAA, SystemC, $textColor="blue", $lineColor="blue", $offsetY="-40", $offsetX="-50")
      UpdateRelStyle(SystemC, customerA, $textColor="red", $lineColor="red", $offsetX="-50", $offsetY="20")

      UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")"}"""

MINDMAP = """Design a Mindmap using Mermaid's intuitive syntax to visually organize and present 
hierarchical information around a central theme. Begin with the root node, symbolizing the main 
idea, and expand outward into branches representing related subtopics and concepts. 
Utilize different shapes like squares, circles, hexagons, and clouds to differentiate between 
various elements of the mindmap. Enhance the nodes with icons and custom classes for a more 
distinctive and visually appealing layout. Incorporate Markdown strings to format the text within
nodes, allowing for bold and italicized text, and ensure the text wraps automatically for longer 
descriptions. The final mindmap should offer a clear, structured, and visually engaging 
representation of the central idea and its associated topics, suitable for brainstorming, 
planning, or presenting complex information in a simplified manner.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "mindmap
  root((mindmap))
    Origins
      Long history
      ::icon(fa fa-book)
      Popularisation
        British popular psychology author Tony Buzan
    Research
      On effectiveness<br/>and features
      On Automatic creation
        Uses
            Creative techniques
            Strategic planning
            Argument mapping
    Tools
      Pen and paper
      Mermaid"}"""

TIMELINE = """Design a Timeline diagram using Mermaid to chronologically depict a series of events
or significant milestones. Start by initializing the diagram with the timeline keyword and 
optionally add a title for contextual clarity. For each event or period in your timeline, specify 
the time or period, followed by a colon, and then describe the event. You can also group events 
into sections for better organization and clarity. To represent multiple events occurring in the 
same period, simply align them vertically under the same time marker. Experiment with customizing 
the color scheme using Mermaid's theme variables to differentiate between sections or individual 
time periods. The final timeline should offer a visually linear and chronological representation 
of events, ideal for historical timelines, project timelines, or any scenario where tracking the 
sequence of events is crucial.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "timeline
    title History of Social Media Platform
    2002 : LinkedIn
    2004 : Facebook
         : Google
    2005 : Youtube
    2006 : Twitter"}"""

SANKEY = """Create a Mermaid SANKEY diagram to visualize the flow of data or resources. Begin your 
diagram with the configuration block to set up the visual properties. Use --- to start the 
configuration, specifying sankey settings such as showValues: false. Follow this with --- and 
sankey-beta to begin the actual diagram. Structure your diagram using a CSV format with 
three columns representing 'source', 'target', and 'value'. Incorporate empty lines for visual 
separation, and employ double quotes for text containing commas or quotes. Adjust linkColor and 
nodeAlignment in the config block for customized aesthetics.
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "---
config:
  sankey:
    showValues: false
---
sankey-beta

Agricultural 'waste',Bio-conversion,124.729
Bio-conversion,Liquid,0.597
Bio-conversion,Losses,26.862
Bio-conversion,Solid,280.322
Bio-conversion,Gas,81.144
Biofuel imports,Liquid,35
Biomass imports,Solid,35
Coal imports,Coal,11.606
Coal reserves,Coal,63.965
Coal,Solid,75.571
District heating,Industry,10.639
District heating,Heating and cooling - commercial,22.505
District heating,Heating and cooling - homes,46.184
Electricity grid,Over generation / exports,104.453
Electricity grid,Heating and cooling - homes,113.726
Electricity grid,H2 conversion,27.14
Electricity grid,Industry,342.165
Electricity grid,Road transport,37.797
Electricity grid,Agriculture,4.412
Electricity grid,Heating and cooling - commercial,40.858
Electricity grid,Losses,56.691
Electricity grid,Rail transport,7.863
Electricity grid,Lighting & appliances - commercial,90.008
Electricity grid,Lighting & appliances - homes,93.494
Gas imports,Ngas,40.719
Gas reserves,Ngas,82.233
Gas,Heating and cooling - commercial,0.129
Gas,Losses,1.401
Gas,Thermal generation,151.891
Gas,Agriculture,2.096
Gas,Industry,48.58
Geothermal,Electricity grid,7.013
H2 conversion,H2,20.897
H2 conversion,Losses,6.242
H2,Road transport,20.897
Hydro,Electricity grid,6.995
Liquid,Industry,121.066"}"""

XYCHART = """Generate UML code for an XY Chart
You can provide the following information:
1. Chart orientation: vertical or horizontal.
2. Title for the chart.
3. X-axis configuration:
   - Title and range (min --> max) for numeric values.
   - Title and list of categorical values in square brackets for categorical values.
4. Y-axis configuration:
   - Title and range (min --> max) for numeric values.
5. Line chart data: a list of numeric values.
6. Bar chart data: a list of numeric values.
7. Always use --- to start the configuration, specifying xyChart settings such as height: 600, width: 1200. Follow this with --- and xychart-beta to begin the actual diagram.
8. Set the width and height in config to fit all values in the xychart
Provide the output in JSON format as follows: {"code": "<correct code here>"}.

Example: {"code": "---
config:
    xyChart:
        width: 1800
        height: 600
    themeVariables:
        xyChart:
            titleColor: "#0000ff"
---
xychart-beta
    title "Sales Revenue"
    x-axis [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
    y-axis "Revenue (in $)" 4000 --> 11000
    bar [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
    line [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]"}"""
