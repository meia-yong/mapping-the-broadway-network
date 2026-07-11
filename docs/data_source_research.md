# Data Source Research

## Objective
Identify a reliable source for historical Broadway production and cast data that can be scraped for this project.

The final dataset requires:

- production title
- production year
- production type
- performer names
- performer-production relationships

The dataset should cover Broadway productions from 1943 (Oklahoma!) onwards.

## Internet Broadway Database (IBDB)

### Findings

IBDB separates Broadway shows from individual Broadway productions.

Example:

Show:
- Oklahoma! (show ID 6697)

Productions:
- Oklahoma! (production ID 1285)
- Oklahoma! revival productions (separate production IDs)

Each production page contains an Opening Night Cast section.

Cast entries include:

- performer name
- role
- performer page links

The dataset therefore naturally supports:

Show → Production → Performer relationships.

### Strengths

- Stable IDs for shows, productions, and performers
- Clear separation between original productions and revivals
- Historical Broadway coverage
- Cast lists include ensemble performers
- Role information available

### Potential challenges

- Role descriptions vary considerably
- Ensemble classification may require cleaning
- Need to verify consistency across decades

## Decision

Chosen primary source:

Internet Broadway Database (IBDB)

Reason:

IBDB provides the most suitable structure for modelling Broadway collaboration networks. It separates shows from individual Broadway productions, provides stable identifiers, distinguishes opening night casts from later replacements, and contains historical cast information across both musicals and plays.

The final dataset will model each Broadway production as a collaboration event using its opening night cast.