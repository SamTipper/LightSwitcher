from datetime import datetime


def time_check(business_hours_start, business_hours_end):
    def decorator(func):
        async def wrapper(ctx, *args, **kwargs):
            current_hour = datetime.now().hour
            print(type(current_hour))

            if current_hour in range(business_hours_start, business_hours_end + 1):
                await func(ctx, *args, **kwargs)
            else:
                await ctx.respond(
                    f"Business hours are from {business_hours_start} to {business_hours_end}."
                )

        return wrapper

    return decorator
