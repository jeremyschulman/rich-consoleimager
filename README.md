# Rich Console-Imager

Do you love Rich and want to create image files from Console output?  I do. I
do this task often as a need to post "pretty-tables" to Slack messages.

This page contains two classes `ConsoleImager` and `TableImager`. The primary
use of creating pretty table images, by example, is shown in the context of
posting the image to Slack via their Bolt framework.  I happen to be using
asyncio.

```python

from slack_bolt.async_app import AsyncBoltRequest
from rich.table import Table
from rich_consoleimager import TableImage

async def demo(table: Table, request: AsyncBoltRequest, slack_channel: str):
    """
    This demonstration is used to create a perfectly fit screen snapshot image of
    the table contents, and the using that image upload to a Slack channel.
    """
    async with TableImage(table) as image:
        await image.render(title=f"This title is at the top of the image")
        await request.context.client.files_upload(
            file=image.image_file, channels=slack_channel,
        )
```
