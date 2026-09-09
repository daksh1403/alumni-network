-- ====================================================================
-- ALUMNI NETWORK AND ENGAGEMENT PLATFORM
-- Part 0: Drop every object from previous runs (old or new layout).
-- Safe to run repeatedly.
-- ====================================================================

BEGIN
    FOR v IN (SELECT view_name FROM user_views
              WHERE view_name IN ('VW_ALUMNI_DIRECTORY', 'VW_MENTORSHIP_SUMMARY',
                                  'VW_EVENT_ATTENDANCE', 'VW_DONATION_TOTALS')) LOOP
        EXECUTE IMMEDIATE 'DROP VIEW ' || v.view_name;
    END LOOP;
END;
/

BEGIN
    FOR o IN (SELECT object_name, object_type FROM user_objects
              WHERE object_type IN ('PROCEDURE', 'FUNCTION', 'PACKAGE')
                AND object_name IN ('PKG_ALUMNI_REPORTS', 'FN_TOTAL_DONATION',
                                    'FN_ALUMNI_SKILL_COUNT', 'PR_REGISTER_ALUMNI_EVENT',
                                    'PR_ADD_SKILL_TO_ALUMNI')) LOOP
        EXECUTE IMMEDIATE 'DROP ' || o.object_type || ' ' || o.object_name;
    END LOOP;
END;
/

BEGIN
    FOR t IN (SELECT trigger_name FROM user_triggers
              WHERE trigger_name LIKE 'TRG\_%' ESCAPE '\') LOOP
        EXECUTE IMMEDIATE 'DROP TRIGGER ' || t.trigger_name;
    END LOOP;
END;
/

BEGIN
    FOR s IN (SELECT sequence_name FROM user_sequences
              WHERE sequence_name LIKE 'SEQ\_%' ESCAPE '\') LOOP
        EXECUTE IMMEDIATE 'DROP SEQUENCE ' || s.sequence_name;
    END LOOP;
END;
/

BEGIN
    FOR t IN (SELECT table_name FROM user_tables
              WHERE table_name IN (
                    -- current ER model (14 relations)
                    'ALUMNI_EVENT', 'ALUMNI_SKILL', 'JOB', 'DONATION', 'EVENT',
                    'MENTORSHIP', 'STUDENT_EMAIL', 'STUDENT', 'ALUMNI_PHONE',
                    'ALUMNI', 'SKILL', 'COMPANY', 'BATCH', 'DEPARTMENT',
                    -- legacy implementation (dropped if still present)
                    'ALUMNI_AUDIT', 'COMMENT_TABLE', 'POST', 'FORUM',
                    'JOB_APPLICATION', 'EVENT_REGISTRATION', 'ADMIN', 'PERSON',
                    'MENTORSHIP_AREA', 'EVENT_TYPE', 'COMPANY_SIZE')
              ORDER BY table_name DESC) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE "' || t.table_name || '" CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;
/
