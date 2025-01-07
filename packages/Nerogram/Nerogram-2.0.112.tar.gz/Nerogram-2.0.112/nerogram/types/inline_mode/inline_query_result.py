#  Nerogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Nerogram.
#
#  Nerogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Nerogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Nerogram.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import nerogram
from nerogram import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~nerogram.types.InlineQueryResultCachedAudio`
    - :obj:`~nerogram.types.InlineQueryResultCachedDocument`
    - :obj:`~nerogram.types.InlineQueryResultCachedAnimation`
    - :obj:`~nerogram.types.InlineQueryResultCachedPhoto`
    - :obj:`~nerogram.types.InlineQueryResultCachedSticker`
    - :obj:`~nerogram.types.InlineQueryResultCachedVideo`
    - :obj:`~nerogram.types.InlineQueryResultCachedVoice`
    - :obj:`~nerogram.types.InlineQueryResultArticle`
    - :obj:`~nerogram.types.InlineQueryResultAudio`
    - :obj:`~nerogram.types.InlineQueryResultContact`
    - :obj:`~nerogram.types.InlineQueryResultDocument`
    - :obj:`~nerogram.types.InlineQueryResultAnimation`
    - :obj:`~nerogram.types.InlineQueryResultLocation`
    - :obj:`~nerogram.types.InlineQueryResultPhoto`
    - :obj:`~nerogram.types.InlineQueryResultVenue`
    - :obj:`~nerogram.types.InlineQueryResultVideo`
    - :obj:`~nerogram.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "nerogram.Client"):
        pass
