-- Write a SQL script that creates a function SafeDiv that divides
-- (and returns) the first by the second number or returns 0 if
-- The second number is equal to 0.
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE res FLOAT DEFAULT 0;

    IF b != 0 THEN
        SET res = a / b;
    END IF;
    RETURN res;
END $$
DELIMITER ;
