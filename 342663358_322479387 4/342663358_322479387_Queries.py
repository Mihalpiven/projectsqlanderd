QUERY_ANSWERS = {
    "Q3":
        """
        select distinct attendance.date
    from attendance
    inner join (
        select C1.name
        from Condition1 C1
        inner join Condition2 C2 on C1.name = C2.name
        inner join Condition3 C3 on C2.name = C3.name
    )
    as PopularContacts
    on attendance.contactName = popularContacts.name
    order by date asc;
        """
    ,
    "Q4":
        """
SELECT C2.name AS name, MIN(A4.date) AS FirstMeetingDate
FROM Contacts C2
INNER JOIN Attendance A4
ON C2.name = A4.contactName
WHERE C2.name IN (
        SELECT C1.name
        FROM Contacts C1
        WHERE C1.city IN (
                SELECT city
                FROM CohesiveCities))
    AND C2.name IN (
        SELECT C3.name
        FROM Contacts C3
        WHERE EXISTS (
                SELECT *
                FROM Attendance A3
                WHERE C2.name = A3.contactName
                    AND A3.date IN (
                        SELECT A1.date
                        FROM Attendance A1
                        WHERE EXISTS (
                                SELECT A2.contactName
                                FROM Attendance A2
                                WHERE A1.date = A2.date
                                    AND A2.contactName IN (
                                        SELECT name
                                        FROM NeatContacts)))))
GROUP BY C2.name;
        """
}
