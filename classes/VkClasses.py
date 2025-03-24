import datetime
class PhotoSize:
    height: int
    size_type: str #type
    width: int
    url: str

    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.size_type = kwargs.get("size_type")

class AttachmentPhoto:
    album_id: int
    date: datetime.datetime
    id: int
    owner_id: int
    access_key: str
    post_id: int
    sizes: list[PhotoSize]
    text: str
    user_id: int
    web_view_token: str
    has_tags: bool
    orig_photo: PhotoSize

    def __init__(self, **kwargs):
        self.album_id = kwargs.get('album_id')
        self.date = kwargs.get('date')
        self.id = kwargs.get('id')
        self.owner_id = kwargs.get('owner_id')
        self.access_key = kwargs.get('access_key')
        self.post_id = kwargs.get('post_id')
        self.sizes = kwargs.get('sizes')
        self.text = kwargs.get('text')
        self.user_id = kwargs.get('user_id')
        self.web_view_token = kwargs.get('web_view_token')
        self.has_tags = kwargs.get('has_tags')
        self.orig_photo = kwargs.get('orig_photo')
        if self.orig_photo != None:
            self.orig_photo = PhotoSize(**self.orig_photo)

class ImageType:
    url: str
    width: int
    height: int
    with_padding: int

    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.with_padding = kwargs.get("with_padding")

class AttachmentVideo:
    response_type: str
    access_key: str
    can_comment: bool
    can_like: bool
    can_repost: bool
    can_subscribe: bool
    can_add_to_faves: bool
    can_add: bool
    comments: int
    date: datetime.datetime
    description: str
    duration: int
    image: ImageType

    def __init__(self, **kwargs):
        self.response_type = kwargs.get('response_type', '')
        self.access_key = kwargs.get('access_key', '')
        self.can_comment = kwargs.get('can_comment', False)
        self.can_like = kwargs.get('can_like', False)
        self.can_repost = kwargs.get('can_repost', False)
        self.can_subscribe = kwargs.get('can_subscribe', False)
        self.can_add_to_faves = kwargs.get('can_add_to_faves', False)
        self.can_add = kwargs.get('can_add', False)
        self.comments = kwargs.get('comments', 0)

        self.date = kwargs.get('date')
        if self.date != None:
            self.date = datetime.datetime.fromtimestamp(self.date)

        self.description = kwargs.get('description', '')
        self.duration = kwargs.get('duration', 0)
        self.image = kwargs.get('image')
        if self.image != None:
            self.image = ImageType(**self.image)

class Attachment:
    _type: str
    video: AttachmentVideo | None
    photo: AttachmentPhoto | None

    def __init__(self, **kwargs):
        self._type = kwargs.get("type", "undef")
        self.video = kwargs.get("video")
        if self.video != None:
            self.video = AttachmentVideo(**self.video)

        self.photo = kwargs.get("photo")
        if self.photo != None:
            self.photo = AttachmentPhoto(**self.photo)

class Wall:
    inner_type: str
    ads_easy_promote: dict
    donut: dict
    is_pinned: bool
    comments: dict
    marked_as_ads: bool
    hashsum: str #hash
    walltype: str #type
    push_subscription: dict
    date: datetime.datetime
    edited: datetime.datetime
    from_id: int
    id: int
    is_favorite: bool
    likes: dict
    reaction_set_id: str
    reactions: dict
    owner_id: int
    post_source: dict
    post_type: str
    reposts: dict
    text: str
    views: dict
    track_code: str
    attachments: list[Attachment]

    def __init__(self, **kwargs):
        self.inner_type = kwargs.get('inner_type', '')
        self.ads_easy_promote = kwargs.get('ads_easy_promote', {})
        self.donut = kwargs.get('donut', {})
        self.is_pinned = kwargs.get('is_pinned')
        if self.is_pinned != None:
            self.is_pinned = bool(self.is_pinned)
        self.comments = kwargs.get('comments', {})
        self.marked_as_ads = kwargs.get('marked_as_ads', False)
        self.hashsum = kwargs.get('hashsum', '')
        self.walltype = kwargs.get('walltype', '')
        self.push_subscription = kwargs.get('push_subscription', {})
        self.date = kwargs.get('date')
        if self.date != None:
            self.date = datetime.datetime.fromtimestamp(self.date)

        self.edited = kwargs.get('edited')
        if self.edited != None:
            self.edited = datetime.datetime.fromtimestamp(self.edited)

        self.from_id = kwargs.get('from_id')
        self.id = kwargs.get('id')
        self.is_favorite = kwargs.get('is_favorite', False)
        self.likes = kwargs.get('likes', {})
        self.reaction_set_id = kwargs.get('reaction_set_id', '')
        self.reactions = kwargs.get('reactions', {})
        self.owner_id = kwargs.get('owner_id')
        self.post_source = kwargs.get('post_source', {})
        self.post_type = kwargs.get('post_type', '')
        self.reposts = kwargs.get('reposts', {})
        self.text = kwargs.get('text', '')
        self.views = kwargs.get('views', {})
        self.track_code = kwargs.get('track_code', '')

        self.attachments = []
        att = kwargs.get('attachments', [])
        if len(att) > 0:
            for attachment in att:
                self.attachments.append(Attachment(**att))