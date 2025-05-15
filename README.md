SatDash: satellite dashboard.

View groundtracks and orbits of active satellites (as tracked by NORAD).
See trends in satellites.
Look up information about the orbits of over 10,000 satellites.

Run etl.py to update the database.
Run sreamlit dashboard.py to see the dashboard.

Dataset used:
https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle
Key works used:
Juan Luis Cano Rodríguez, Jorge Martinez, et al.. (2023). poliastro: poliastro 0.17.0. Zenodo. 10.5281/zenodo.6817189
Vallado, David A., Paul Crawford, Richard Hujsak, and T.S. Kelso, "Revisiting Spacetrack Report #3," presented at the AIAA/AAS Astrodynamics Specialist Conference, Keystone, CO, 2006 August 21–24. 10.2514/6.2006-6753
Vallado, David A., 2001. Fundamentals of astrodynamics and applications (Vol. 12). Springer Science & Business Media.

Investigated:
What obrital mechanics are demonstrated in this data?
Are high inclination orbits unpopular?
How dominant is LEO?

Answers:
The relationship between revolution rate and semi-major axis is demonstrated clearly.
The relationship between velocity and semi-major axis did not show at all.
Medium inclination orbits (~45 degrees) are common, presumably to cover most of the planet (excluding the poles).
Almost all satellites are in LEO, and were launched in the last 5 years.

When the size of the dataset increases, consider the optimisations:
Precomputing regular ephemerides with SGP4, and interpolating with propagation model that does not account for drag.
Precomputing ephemerides server-side (very expensive though). Perhaps only for frequently viewed satellites.

Security and privacy concerns:
No privacy concerns (unless you count doxxing the astronauts on the ISS), as all data is publicly available and has not been enriched to provide private information.
Security concerns, database that stores transformed data must be kept secure. Low stakes, but nobody likes services being degraded/defaced.

How to transfer onto AWS:
The etl pipeline is lightweight enough to run as a Lambda daily. The database (being non-relational) could be changed to run on DynamoDB. The streamlit app could run on EC2, only being instanced by Fargate when CloudWatch detects a DNS hit on Route53 and triggers a Lambda to temporarily set the Fargate service's task count to 1. This would be dirt cheap to run.
