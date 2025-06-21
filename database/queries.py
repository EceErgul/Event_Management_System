# All database operations (CRUD queries)

from .db_connection import get_connection

def fetch_all_events():
    query = """
        SELECT e.EventID, e.Name, e.Date, e.Location, o.Name AS OrganizerName
        FROM Event e
        JOIN Organizer o ON e.OrganizerID = o.OrganizerID
        ORDER BY e.Date;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_participants_by_event(event_id):
    query = """
        SELECT p.ParticipantID, p.Name, p.Email, r.Status, r.Attendance
        FROM Registration r
        JOIN Participant p ON r.ParticipantID = p.ParticipantID
        WHERE r.EventID = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (event_id,))
            return cur.fetchall()

def update_event(event_id, name, date, location, organizer_id):
    query = """
        UPDATE Event
        SET Name=%s, Date=%s, Location=%s, OrganizerID=%s
        WHERE EventID=%s;
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, date, location, int(organizer_id), event_id))
                conn.commit()
        return True
    except Exception as e:
        print("Error updating event:", e)
        return False
    
def update_participant(pid, name, email, contact, department_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE Participant
                    SET Name=%s, Email=%s, Contact=%s, DepartmentID=%s
                    WHERE ParticipantID=%s
                """, (name, email, contact, department_id, pid))
                conn.commit()
        return True
    except Exception as e:
        print("Update Participant Error:", e)
        return False

def delete_event(event_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Registration WHERE EventID = %s", (event_id,))
                cur.execute("DELETE FROM Event WHERE EventID = %s", (event_id,))
                conn.commit()
        return True
    except Exception as e:
        print("Failed to delete event:", e)
        return False

def delete_participant(participant_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Registration WHERE ParticipantID = %s", (participant_id,))
                cur.execute("DELETE FROM Participant WHERE ParticipantID = %s", (participant_id,))
                conn.commit()
        return True
    except Exception as e:
        print("Failed to delete participant:", e)
        return False
    
def insert_event(name, date, location, organizer_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Event (Name, Date, Location, OrganizerID)
                    VALUES (%s, %s, %s, %s)
                """, (name, date, location, organizer_id))
                conn.commit()
        return True
    except Exception as e:
        print("Insert Event Error:", e)
        return False
    
def fetch_all_participants():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT ParticipantID, Name, Email, Contact, DepartmentID
                    FROM Participant
                    ORDER BY Name
                """)
                return cur.fetchall()
    except Exception as e:
        print("Error fetching participants:", e)
        return []
    
def insert_participant(name, email, contact, department_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Participant (Name, Email, Contact, DepartmentID)
                    VALUES (%s, %s, %s, %s)
                """, (name, email, contact, department_id))
                conn.commit()
        return True
    except Exception as e:
        print("Insert Participant Error:", e)
        return False

def insert_event_registration(event_id, name, email, status, attendance):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Participant (Name, Email, Contact, DepartmentID)
                    VALUES (%s, %s, '', 1) RETURNING ParticipantID
                """, (name, email))
                pid = cur.fetchone()[0]
                cur.execute("""
                    INSERT INTO Registration (EventID, ParticipantID, Status, Attendance)
                    VALUES (%s, %s, %s, %s)
                """, (event_id, pid, status, attendance))
                conn.commit()
        return True
    except Exception as e:
        print("Insert Registration Error:", e)
        return False

def update_event_registration(participant_id, name, email, status, attendance):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE Participant SET Name=%s, Email=%s WHERE ParticipantID=%s;
                    UPDATE Registration SET Status=%s, Attendance=%s
                    WHERE ParticipantID=%s;
                """, (name, email, participant_id, status, attendance, participant_id))
                conn.commit()
        return True
    except Exception as e:
        print("Update Registration Error:", e)
        return False

def delete_event_registration(participant_id, event_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM Registration
                    WHERE ParticipantID = %s AND EventID = %s;
                """, (participant_id, event_id))
                conn.commit()
        return True
    except Exception as e:
        print("Delete Registration Error:", e)
        return False