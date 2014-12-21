def build_url(url, **kwargs):
    import urllib
    removed_kwargs = {}
    for key in kwargs:
        if kwargs[key] is not None:
            removed_kwargs[key] = kwargs[key]

    params = urllib.parse.urlencode(removed_kwargs)
    return url + "?%s" % params


def redirect_link_with_params(url_name, *args, **kwargs):
    from django.core.urlresolvers import reverse
    url = reverse(url_name, args=args)
    return build_url(url, **kwargs)


def last_liked(article, reader):
    try:
        record = ReadRecord.objects.filter(reader=reader, article=article).latest("read_at")
        return record.liked
    except ReadRecord.DoesNotExist:
        pass
    return False
