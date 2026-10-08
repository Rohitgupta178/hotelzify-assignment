def last_n_days_revenue(daily, n):
    return sum(daily[-n:])


def cancellation_rate(bookings):
    if not bookings:
        return 0.0

    cancelled = sum(
        1 for b in bookings
        if b["status"].lower() == "cancelled"
    )

    return cancelled / len(bookings) * 100


# Test 1
daily = [100, 200, 300, 400, 500]
print("Last 3 days revenue:", last_n_days_revenue(daily, 3))


# Test 2
bookings = [
    {"status": "confirmed"},
    {"status": "cancelled"},
    {"status": "confirmed"},
    {"status": "cancelled"},
]

print("Cancellation rate:", cancellation_rate(bookings))


# Test 3 - empty bookings
print("Empty cancellation rate:", cancellation_rate([]))