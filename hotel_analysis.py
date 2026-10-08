import pandas as pd


# -----------------------------
# 1. Load the booking data
# -----------------------------
data = [
    ["B1001", "12/10/2026", "Booking.com", 120, "confirmed"],
    ["B1002", "2026-10-13", "booking com", 95, "cancelled"],
    ["B1003", "Oct 14 2026", "Direct", 110, "confirmed"],
    ["B1003", "Oct 14 2026", "Direct", 110, "confirmed"],
    ["B1004", "15-10-2026", "BDC", 140, "confirmed"],
    ["B1005", "2026-10-18", "Expedia", 200, "confirmed"],
    ["B1006", "18/10/2026", "expedia", 180, "cancelled"],
    ["B1007", "2026-11-02", "Direct", 130, "confirmed"],
    ["B1008", "02/11/2026", "Booking.com", 150, "confirmed"],
    ["B1008", "02/11/2026", "Booking.com", 150, "confirmed"],
    ["B1009", "Nov 05 2026", "EXPEDIA", 175, "confirmed"],
    ["B1010", "2026-11-07", "Direct", 90, "cancelled"],
    ["B1011", "07-11-2026", "bdc", 160, "confirmed"],
]

columns = ["id", "check_in", "channel", "amount", "status"]

df = pd.DataFrame(data, columns=columns)


# -----------------------------
# 2. Remove duplicate rows
# -----------------------------
df = df.drop_duplicates()


# -----------------------------
# 3. Normalize channel names
# -----------------------------
channel_map = {
    "booking.com": "Booking.com",
    "booking com": "Booking.com",
    "bdc": "Booking.com",
    "expedia": "Expedia",
    "direct": "Direct",
}

df["channel"] = (
    df["channel"]
    .str.strip()
    .str.lower()
    .map(channel_map)
)


# -----------------------------
# 4. Parse mixed date formats
# -----------------------------
def parse_date(value):
    value = str(value).strip()

    # ISO format: YYYY-MM-DD
    if value[0:4].isdigit() and value[4] == "-":
        return pd.to_datetime(value, format="%Y-%m-%d")

    # Other formats: interpret ambiguous dates as DD/MM/YYYY
    return pd.to_datetime(
        value,
        format="mixed",
        dayfirst=True
    )


df["check_in"] = df["check_in"].map(parse_date)

df["month"] = df["check_in"].dt.to_period("M")


# -----------------------------
# 5. Calculate net revenue
#    Exclude cancelled bookings
# -----------------------------
confirmed = df[df["status"].str.lower() == "confirmed"]

revenue = (
    confirmed
    .groupby(["month", "channel"])["amount"]
    .sum()
    .reset_index()
)

print("\nNET REVENUE BY CHANNEL BY MONTH")
print(revenue.to_string(index=False))


# -----------------------------
# 6. Calculate cancellation rate
# -----------------------------
cancellation_rate = (
    df.groupby("channel")["status"]
    .apply(
        lambda status:
        (status.str.lower() == "cancelled").mean() * 100
    )
    .reset_index(name="cancellation_rate_%")
)

print("\nCANCELLATION RATE BY CHANNEL")
print(cancellation_rate.to_string(index=False))