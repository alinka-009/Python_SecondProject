from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from datetime import datetime, timedelta
import calendar

calendar_callback = CallbackData('calendar', 'act', 'year', 'month', 'day')


def create_calendar(year=datetime.now().year, month=datetime.now().month):
    """
    Creates an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns InlineKeyboardMarkup object with the calendar.
    """
    inline_kb = InlineKeyboardMarkup(row_width=7)
    ignore_callback = calendar_callback.new("IGNORE", year, month, 0)  # for buttons with no answer
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(f'{calendar.month_name[month]} {str(year)}', callback_data=ignore_callback))
    inline_kb.row()
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        inline_kb.insert(InlineKeyboardButton(day, callback_data=ignore_callback))

    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        inline_kb.row()
        for day in week:
            if day == 0:
                inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
            else:
                inline_kb.insert(InlineKeyboardButton(str(day), callback_data=calendar_callback.new("DAY", year, month, day)))

    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton("<", callback_data=calendar_callback.new("PREV-MONTH", year, month, day)))
    inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
    inline_kb.insert(InlineKeyboardButton(">", callback_data=calendar_callback.new("NEXT-MONTH", year, month, day)))

    return inline_kb


async def process_calendar_selection(query, data):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param query: callback_query, as provided by the CallbackQueryHandler
    :param data: callback_data, dictionary, set by calendar_callback
    :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                and returning the date if so.
    """
    return_data = (False, None)
    temp_date = datetime(int(data['year']), int(data['month']), 1)
    if data['act'] == "IGNORE":
        await query.answer(cache_time=60)
    elif data['act'] == "DAY":
        await query.message.delete_reply_markup()   # removing inline keyboard
        return_data = True, datetime(int(data['year']), int(data['month']), int(data['day']))
    elif data['act'] == "PREV-YEAR":
        prev_date = temp_date - timedelta(days=365)
        await query.message.edit_reply_markup(create_calendar(int(prev_date.year), int(prev_date.month)))
    elif data['act'] == "NEXT-YEAR":
        next_date = temp_date + timedelta(days=365)
        await query.message.edit_reply_markup(create_calendar(int(next_date.year), int(next_date.month)))
    elif data['act'] == "PREV-MONTH":
        prev_date = temp_date - timedelta(days=1)
        await query.message.edit_reply_markup(create_calendar(int(prev_date.year), int(prev_date.month)))
    elif data['act'] == "NEXT-MONTH":
        next_date = temp_date + timedelta(days=31)
        await query.message.edit_reply_markup(create_calendar(int(next_date.year), int(next_date.month)))
    else:
        await query.message.answer("Something went wrong!")

    # at some point user clicks DAY button, returning date
    return return_data
