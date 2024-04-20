import mysql.connector

def store_data(ph, tds, temp, turbidity, longitude, latitude, motorState):
    mydb = mysql.connector.connect(
        host="localhost",
        user="python",
        password="python123!",
        database="ETAS_IOT"
    )

    mycursor = mydb.cursor()

    try:
        # Convert motorState to int
        motorState = int(motorState)

        sql = "INSERT INTO datalogs (`phValue`, `tdsValue`, `tempValue`, `turbidityValue`, `longitude`, `latitude`, `motorState`, `deviceID`) VALUES (%s, %s, %s, %s, %s, %s, %s, 'ABC123');"
        val = (ph, tds, temp, turbidity, longitude, latitude, motorState)
        mycursor.execute(sql, val)
        mydb.commit()
        print("\nValues inserted successfully\n")
    except mysql.connector.Error as e:
        print("\nI couldn't add the data to the database\n\nError: {}".format(e))
