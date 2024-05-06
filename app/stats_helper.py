from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_top_camera_make(db: Session, n: int = 10) -> list[str]:
    query = text(
        """SELECT a.value || ' - ' ||b.value, COUNT(1) 
        FROM image_metadata a 
        JOIN image_metadata b 
            ON (a.tag = 'Make' 
            AND b.tag = 'Model' 
            AND a.image_id = b.image_id) 
        GROUP BY 1 
        ORDER BY 2 DESC
        LIMIT :num;"""
    )
    result = db.execute(query, {"num": n}).fetchall()
    top_make = [record[0] for record in result]
    return top_make


def get_top_image_format(db: Session, n: int = 1) -> list[str]:
    query = text(
        """SELECT value, COUNT(1)
        FROM image_metadata
        WHERE tag = 'ImageFormat'
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT :num;"""
    )
    result = db.execute(query, {"num": n}).fetchall()
    top_image_format = [record[0] for record in result]
    return top_image_format


def get_image_upload_frequency(db: Session, n=30) -> dict[str, int]:
    query = text(
        """SELECT date(created_time, 'unixepoch'), count(1) 
                 FROM uploaded_images 
                 ORDER BY 1 DESC 
                 LIMIT :num;"""
    )
    result = db.execute(query, {"num": n}).fetchall()
    upload_freq = {date: freq for date, freq in result}
    return upload_freq


def get_stats(db: Session) -> dict[str, list[str] | str | dict[str, int]]:
    stats = {}

    stats["Top 10 Popular Camera Models"] = get_top_camera_make(db=db)

    top_image_format = get_top_image_format(db=db)
    most_popular_image_format = "-"
    if top_image_format:
        most_popular_image_format = top_image_format[0]
    stats["Most Popular Image Format"] = most_popular_image_format

    stats["Image Upload Frequency Per Day (last 30 days)"] = get_image_upload_frequency(
        db=db
    )
    return stats
