# azuracast-sse-client
An SSE-driven Azuracast metadata client

# Why this app
This client connects to an Azuracast SSE client and captures the high-frequency
metadata updates from the Azuracast server. You supply a callback that will be
given the current metadata. The client runs continuously until stopped.

# Configuration
    client = build_sse_client(servername, shortcode, downtimeDJName)
    client.run(callback)

 - `servername`: the target Azuracast server name as a string.
 - `shortcode`: the radio station ID, from the station's profile page on the Azuracast server.
 - `downtimeDJName`: if you play tracks automatically from the library, this "DJ" name will be supplied as the default DJ.
 - `callback`: your processing code. You will receive a `NowPlayingResponse` object (q.v.).

## Environment variables
 - `AZ_CLIENT_DEBUG`: Set this to any non-null value to enable logging of the extracted metadata as it arrives.
 
# NowPlayingResponse
The `NowPlayingResponse` object contains the parsed metadata from the current SSE event. The 0.1.x version
of this module returns the current song info and any available streamer data only. The SSE event contains
quite a lot more information, but I only needed a subset of the fields:
 - `artist`: artist name for current song
 - `track`: track name for current song
 - `album`: album name of current song
 - `dj`: current streamer's name, or the default DJ name if Azuracast is playing from the media library
 - `live`: `True` if there is a live streamer, `False` if not
 - `duration`: length of the current track in `hh:mm:ss` format
 - `elapsed`: how long the track has been playing
 - `start`: `datetime` that the track started playing
 - `artURL`: a URL pointing to the track artwork, or a generic cover image supplied by Azuracast if no track artwork is available

# Using the client
The client works best if you are setting up a long-running monitor to watch the SSE data and update
a display (e.g., sending the data to a Discord channel). It can be run in bursts to fetch the current data,
but the `AzuracastPy` library is a better fit for one-off requests.
