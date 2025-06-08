VIEWS_DICT = {
    "Q3":
        [
		"""
create view Popularity as
select name, count(*) as popularityLevel
from Contacts
         inner join CommonContacts
                    on Contacts.name = CommonContacts.savedContact
group by name;
""",

"""
create view Condition1 as
select contactSaver as name
from CommonContacts
         inner join Contacts
                    on CommonContacts.savedContact = Contacts.name
group by contactSaver
having count(distinct city) >= 2;
		""",
        """
        create view Condition2 as
SELECT contactSaver as name
FROM CommonContacts
WHERE contactSaver IN (SELECT CC1.contactSaver
                       FROM CommonContacts CC1
                                INNER JOIN CommonContacts CC2
                                           ON CC1.savedContact = CC2.contactSaver AND
                                              CC1.contactSaver = CC2.savedContact
                       GROUP BY CC1.contactSaver
                       HAVING COUNT(*) = (SELECT COUNT(*)
                                          FROM CommonContacts CC3
                                          WHERE CC3.contactSaver = CC1.contactSaver));
        """,
        """
        create view Condition3 as
select CC1.contactSaver as name
from CommonContacts CC1
         inner join Popularity P1
                    on CC1.contactSaver = P1.name
where not exists (select *
                  from CommonContacts CC2
                           inner join Popularity P2
                                      on CC2.savedContact = P2.name
                  where CC1.contactSaver = CC2.contactSaver
                    and P1.popularityLevel < P2.popularityLevel);
        """
        ]
    ,
    "Q4":
        [
		"""
CREATE VIEW CohesiveCities AS
SELECT PC.city AS city
FROM (SELECT city, COUNT(*) AS Population
    FROM Contacts
    GROUP BY city) AS PC
LEFT JOIN (
    SELECT C1.city AS city, COUNT(*) AS RelationshipCount
    FROM CommonContacts CC1
    INNER JOIN Contacts C1
    ON CC1.contactSaver = C1.name
    INNER JOIN Contacts C2
    ON CC1.savedContact = C2.name
    WHERE C1.city = C2.city
    GROUP BY C1.city)
AS RC
ON PC.city = RC.city
WHERE RC.RelationshipCount = (PC.Population * (PC.Population - 1))
    OR PC.Population = 1;
		""",
        """
        CREATE VIEW NeatContacts AS
SELECT C3.name AS name
FROM Contacts C3
WHERE C3.name IN (
        SELECT C1.name
        FROM Contacts C1
        WHERE NOT EXISTS (SELECT *
                        FROM CommonContacts CC
                        WHERE CC.contactSaver = C1.name
                        AND CC.nickname != CC.savedContact))
    AND C3.name IN (
        SELECT C2.name
        FROM Contacts C2
        WHERE NOT EXISTS (
                SELECT *
                FROM Attendance A
                WHERE A.contactName = C2.name
                    AND A.delay > 50
            ));
        """
        ]
}



















