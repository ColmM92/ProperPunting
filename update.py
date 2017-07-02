"""
@author: lorrieq
"""


import datetime as dt
from db_interact.common import nonSelectQuery
from db_interact import select


def removeKellyGrowth(sport, date):
    query = "DELETE f FROM fact f JOIN dimEntity e ON f.F_E_ID=e.E_ID " \
            "JOIN dimVenue v ON e.E_VN_ID=v.VN_ID " \
            "JOIN dimValueType vt ON vt.VT_ID=f.F_VT_ID AND vt.VT_Name " \
            "IN ('Kelly', 'Growth') WHERE v.VN_S_ID=%s AND " \
            "date(v.VN_Datetime)=%s;"
    nonSelectQuery(query, (sport, date))


def removeWeekKellyGrowth(sportName):
    today = dt.date.today()
    weekStart = today - dt.timedelta(days=today.weekday())
    weekEnd = weekStart + dt.timedelta(days=6)
    query = "DELETE f FROM fact f JOIN dimEntity e ON f.F_E_ID=e.E_ID " \
            "JOIN dimVenue v ON e.E_VN_ID=v.VN_ID " \
            "JOIN dimValueType vt ON vt.VT_ID=f.F_VT_ID AND vt.VT_Name " \
            "IN ('Kelly', 'Growth') " \
            "JOIN dimSport s ON s.S_ID=v.VN_S_ID AND s.S_Name=%s " \
            "WHERE v.VN_Datetime BETWEEN %s AND %s;"
    nonSelectQuery(query, (sportName, weekStart, weekEnd))


def entityStatus(entityName, date, sport, newStatus):
    eId = select.entityId(entityName, date, sport)
    query = "UPDATE dimEntity SET E_ST_ID=%s WHERE E_ID=%s"
    nonSelectQuery(query, (newStatus, eId))


def venueDatetime(venueId, datenTime):
    query = "UPDATE dimVenue SET VN_Datetime=%s WHERE VN_ID=%s"
    nonSelectQuery(query, (datenTime, venueId))
