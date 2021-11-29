-- Create BMIReference Table
CREATE TABLE BMIreference
         (ID                          INT PRIMARY KEY         NOT NULL,
         BMI_category                 TEXT                    NOT NULL,
         BMI_range_lower              NUMERIC                    NOT NULL,
         BMI_range_upper              NUMERIC                    NULL,
         health_risk                  TEXT                    NOT NULL
         );