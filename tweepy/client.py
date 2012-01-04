import sys
import requests
from urlparse import urljoin

from tweepy import TweepyError
from tweepy.parsers import JSONParser


class Client(object):

    def __init__(self,
        auth=None,
        host='twitter.com',
        secure=True,
        parser=JSONParser(),
        raw_response=None):
        """Create a new client object.

        auth -- A tuple that takes the format:
                    (auth_mode, param_1, param_2, ..., param_n).
                These modes of authentication are supported: OAuth, Basic.
        host -- Hostname of the API server. Defaults to api.twitter.com
        secure -- Uses HTTPS if true (default), otherwise HTTP if false.
        parser -- Parses the responses from the server. (Default: JSONParser)
        raw_response -- If specified no parsing will be performed on
                        the server's response content. Instead the raw
                        data in the requested format will be returned.
                        Examples: json, xml, atom
        """
        self.base_url = '%s://%%s.%s/' % ('https' if secure else 'http', host)
        self.session = requests.session(auth=auth, config={'verbose': sys.stdout})

        if raw_response:
            self.response_format = raw_response
        else:
            self.response_format = parser.response_format
            self.parser = parser

    def request(self, method, url, parameters={}, files=None, subdomain='api'):
        """Send a request to API server.

        method: type of HTTP method to send (ex: GET, DELETE, POST)
        url: API endpoint URL minus the /<version> part.
        parameters: API parameters to be sent with the request.
        """
        base_url = self.base_url % subdomain
        url = '%s.%s' % (urljoin(base_url, url), self.response_format)

        try:
            r = self.session.request(method, url, params=dict(parameters), files=files)
        except requests.exceptions.RequestException, e:
            raise TweepyError('Request error: %s' % e)

        if r.status_code != 200:
            error_msg = self.parser.parse_error(r.content)
            raise TweepyError('API error: %s' % error_msg)

        if self.parser and len(r.content) > 0:
            return self.parser.parse_content(r.content)
        else:
            return r.content

    def home_timeline(self, **parameters):
        """Returns the most recent statuses, including retweets, posted by
           the authenticating user and the user's they follow.

        Returns: List of status objects.
        """
        return self.request('GET', '1/statuses/home_timeline', paramters)

    def mentions(self, **parameters):
        """Returns the most recent mentions (status containing @username) for
           the autenticating user.

        Returns: List of status objects.
        """
        return self.request('GET', '1/statuses/mentions', parameters)

    def public_timeline(self, **parameters):
        """Returns the most recent statuses, including retweets, from
           non-protected users. The public timeline is cached for 60 seconds.

        Returns: List of status objects.
        """
        return self.request('GET', '1/statuses/public_timeline', parameters)

    def retweeted_by_me(self, **parameters):
        """Returns the most recent retweets posted by the authenticating user.

        Returns: List of status objects.
        """
        return self.request('GET', '1/statuses/retweeted_by_me', parameters)

    def retweeted_to_me(self, **parameters):
        """Returns the most recent retweets posted by the users the
           authenticating user follows.

        Returns: List of status objects.
        """
        return self.request('GET', '1/statuses/retweeted_to_me', parameters)

    def retweets_of_me(self, **parameters):
        """Returns the most recent tweets of the authenticated user
           that have been retweeted by others.

        Returns: List of status objects.
        """
        return self.request('GET', '1/statuses/retweets_of_me', parameters)

    def user_timeline(self, user=None, **parameters):
        """Returns the most recent statuses posted by the authenticating user.
           It is also possible to specify the user to return results for.

        user -- (optional) Screen name or ID of the user for whom
                           to return results for.

        Returns: List of status objects.
        """
        if user:
            url = '1/statuses/user_timeline/%s' % user
        else:
            url = '1/statuses/user_timeline'
        return self.request('GET', url, parameters)

    def retweeted_to_user(self, user=None, **parameters):
        """Returns the most recent retweets posted by users the specified user
           follows. Identical to retweeted_to_me, but allows providing user.

        user -- The ID or screen name of the user for whom to return results.

        Returns: List of status objects.
        """
        parameters['id'] = user
        return self.request('GET', '1/statuses/retweeted_to_user', parameters)

    def retweeted_by_user(self, user=None, **parameters):
        """Returns the most recent retweets posted by the specified user.
           Identical to retweeted_by_me except you can choose the user.

        user -- The ID or screen name of the user for whom to return results.

        Returns: List of status objects.
        """
        parameters['id'] = user
        return self.request('GET', '1/statuses/retweeted_by_user', parameters)

    def retweeted_by(self, status_id, only_ids=False, **parameters):
        """Show user objects up to 100 members who retweeted the status.

        status_id -- The numerical ID of the desired status.
        only_ids -- (optional) If true only returns the user IDs, otherwise
                    by default user objects will be returned.

        Returns: List of user objects or IDs (if only_ids is true).
        """
        if only_ids:
            url = '1/statuses/%s/retweeted_by/ids'
        else:
            url = '1/statuses/%s/retweeted_by'
        return self.request('GET', url % status_id, parameters)

    def retweets(self, status_id, **parameters):
        """Returns up to 100 of the first retweets of a given tweet.

        status_id -- The numerical ID of the desired status.

        Returns: List of status objects.
        """
        url = '1/statuses/retweets/%s' % status_id
        return self.request('GET', url, parameters)

    def show_status(self, status_id, **parameters):
        """Returns a single status by ID.

        status_id -- The numerical ID of the desired status.

        Returns: A status object.
        """
        url = '1/statuses/show/%s' % status_id
        return self.request('GET', url, parameters)

    def destroy_status(self, status_id, **parameters):
        """Destroys the status specified by ID. Authenticating user
           must be the author of the specified status.

        status_id -- The numerical ID of the status to be deleted.

        Returns: A status object which was deleted.
        """
        url = '1/statuses/destroy/%s' % status_id
        return self.request('POST', url, parameters)

    def retweet(self, status_id, **parameters):
        """Retweets a tweet. Returns the original tweet with
           retweet details embedded.

        status_id -- The numerical ID of the status to be retweeted.

        Returns: A status object.
        """
        url = '1/statuses/retweet/%s' % status_id
        return self.request('POST', url, parameters)

    def update_status(self, status, media=None, **parameters):
        """Updates the authenticating user's status (aka tweeting).

        status -- The text of your status update.
        media -- (optional) A path to a file or a tuple with format:
                    (filename, file-like-object)
                 The file will be uploaded as a media attachment for
                 the new status update. Must be of type supported by
                 the API server (ex: jpg, gif, png).

        Returns: A status object.
        """
        parameters['status'] = status

        if isinstance(media, str):
            media = (media, open(media, 'rb'))
        if isinstance(media, tuple):
            return self.request('POST',
                                '1/statuses/update_with_media',
                                parameters,
                                files={'media[]': media},
                                subdomain='upload')

        return self.request('POST', '1/statuses/update', parameters)

    def oembed_status(self, status_id, **parameters):
        """Returns information allowing the creation of an embedded
           representation of a status. See the oEmbed spec for more details.

        status_id -- The status ID to return embed code for.

        Returns: A oEmbed object.
        """
        parameters['id'] = status_id
        return self.request('GET', '1/statuses/oembed', parameters)

    def search(self, query, **parameters):
        """Returns tweets that match a specified query.

        query -- Search query.

        Returns: A search result object.
        """
        parameters['q'] = query
        return self.request('GET', 'search', parameters, subdomain='search')

    def direct_messages(self, **parameters):
        """Returns the most recent direct messages sent
           to the authenticating user.

        Returns: A list of direct message objects.
        """
        return self.request('GET', '1/direct_messages', parameters)

    def direct_messages_sent(self, **parameters):
        """Returns the most recent direct messages sent by
           the authenticating user.

        Returns: A list of direct message objects.
        """
        return self.request('GET', '1/direct_messages/sent', parameters)

    def destroy_direct_message(self, message_id, **parameters):
        """Destroys the direct message specified by the ID.

        message_id -- The ID of the direct message to delete.

        Returns: A direct message object (that was deleted).
        """
        url = '1/direct_messages/destroy/%s' % message_id
        return self.request('POST', url, parameters)

    def send_direct_message(self, text, user=None, **parameters):
        """Send a new direct message to the specified user.

        text -- The text of your direct message.
        user -- The ID or screen name of the user who
                should receive the direct message.

        Returns: A direct message object (which was sent).
        """
        parameters.update({'text': text, 'user': user})
        return self.request('POST', '1/direct_messages/new', parameters)

    def show_direct_message(self, message_id):
        """Returns a single direct message specified by ID.

        message_id -- The ID of the direct message to return.

        Returns: A direct message object.
        """
        return self.request('GET', '1/direct_messages/show/%s' % message_id)

    def followers(self, user=None, **parameters):
        """Returns an array of numeric IDs for every user
           following the specified user.

        user -- The ID or screen name of the user for
                whom to return results for.

        Returns: A list of IDs.
        """
        parameters['user'] = user
        return self.request('GET', '1/followers/ids', parameters)

    def friends(self, user=None, **parameters):
        """Returns an array of numeric IDs for every user
           the specified user is following.

        user -- The ID or screen name of the user for
                whom to return results for.

        Returns: A list of IDs.
        """
        parameters['user'] = user
        return self.request('GET', '1/friends/ids', parameters)

    def friendship_exists(self, user_a, user_b, **parameters):
        """Test for the existence of friendship between two users.

        user_a -- The user you are checking the relationship from.
        user_b -- The user you are checking the relationship to.

        Returns: True if user_a follows user_b, otherwise False.
        """
        parameters.update({'user_a': user_a, 'user_b': user_b})
        return self.request('GET', '1/friendships/exists', parameters)

    def incoming_friendships(self, **parameters):
        """Returns an array of numeric IDs for every user who has a
           pending request to follow the authenticating user.

        Returns: A list of IDs.
        """
        return self.request('GET', '1/friendships/incoming', parameters)

    def outgoing_friendships(self, **parameters):
        """Returns an array of numeric IDs for every protected user for whom
           the authenticating user has a pending follow request.

        Returns: A list of IDs.
        """
        return self.request('GET', '1/friendships/outgoing', parameters)

    def show_friendship(self, source=None, target=None, **parameters):
        """Returns detailed information about the relationship
           between two users.

        source -- The screen name of the subject user.
            OR
        source_id -- The ID of the subject user.

        target -- The screen name of the target user.
            OR
        target_id -- The ID of the target user.

        Returns: A friendship information object.
        """
        parameters.update({'source_screen_name': source,
                           'target_screen_name': target})
        return self.request('GET', '1/friendships/show', parameters)

    def create_friendship(self, user, **parameters):
        """Allows the authenticating user to follow an user.

        user -- The ID or screen name of the user to follow.

        Return: An user object.
        """
        if user:
            url = '1/friendships/create/%s' % user
        else:
            url = '1/friendships/create'
        return self.request('POST', url, parameters)

    def destroy_friendship(self, user, **parameters):
        """Allows the authenticating user to unfollow an user.

        user -- The ID or screen name of the user to unfollow.

        Returns: An user object.
        """
        if user:
            url = '1/friendships/destroy/%s' % user
        else:
            url = '1/friendships/destroy'
        return self.request('POST', url, parameters)

    def lookup_friendships(self, users=None, user_ids=None, **parameters):
        """Returns the relationship of the authenticating user to the
           list of users provided. Values of connections can be:
           following, following_requested, followed_by, and none.

        users -- A list of screen names of users to request. (max 100)
        user_ids -- A list of IDs of users to request. (max 100)

        Returns: A list of relationship objects.
        """
        if users:
            parameters['screen_name'] = ','.join(users)
        if user_ids:
            parameters['user_id'] = ','.join([str(ID) for ID in user_ids])
        return self.request('GET', '1/friendships/lookup', parameters)

    def update_friendship(self, user, device=None, retweets=None, **parameters):
        """Allows one to enable or disable retweets and device notifications
           from the specified user.

        user -- The user for whom to update friendship.
        """
        parameters.update({'screen_name': user,
                           'device': device,
                           'retweets': retweets})
        return self.request('POST', '1/friendships/update', parameters)

    def no_retweet_friendships(self, **parameters):
        """Returns an array of user IDs that the currently authenticated
           user does not want to see retweets from.

        Returns: List of IDs.
        """
        return self.request('GET', '1/friendships/no_retweet_ids', parameters)

    def lookup_users(self, users=None, user_ids=None, **parameters):
        """Returns up to 100 users worth of extended information for a
           list of user screen names or IDs.

        users -- A list of user screen names to request. (max 100)
        user_ids -- A list of user IDs to request. (max 100)

        Returns: A list of user objects.
        """
        if users:
            parameters['screen_name'] = ','.join(users)
        if user_ids:
            parameters['user_id'] = ','.join([str(ID) for ID in user_ids])
        return self.request('GET', '1/users/lookup', parameters)

    # TODO: implement users/profile_image/:screen_name

    def search_users(self, query, **parameters):
        """Runs a search for users.

        query -- The search query to run against people search.

        Returns: A list of user objects.
        """
        parameters['q'] = query
        return self.request('GET', '1/users/search', parameters)

    def show_user(self, user=None, **parameters):
        """Returns extended information of a given user.

        user -- The screen name of the user for whom to return results for.

        Returns: An user object.
        """
        parameters['screen_name'] = user
        return self.request('GET', '1/users/show', parameters)

    def contributees(self, user=None, **parameters):
        """Returns users that the specified user can contribute to.

        user -- The screen name of the user for whom to return results for.

        Returns: A list of user objects.
        """
        parameters['screen_name'] = user
        return self.request('GET', '1/users/contributees', parameters)

    def contributors(self, user=None, **parameters):
        """Returns users who can contribute to the specified account.

        user -- The screen name of the user for whom to return results for.

        Returns: A list of user objects.
        """
        parameters['screen_name'] = user
        return self.request('GET', '1/users/contributors', parameters)

    def user_suggestion_categories(self, **parameters):
        """Returns a list of user categories. The category can then
           be passed to user_suggestions() to get a list of suggested users
           for that specified catgeory.

        Returns: A list of category objects.
        """
        return self.request('GET', '1/users/suggestions', parameters)

    def user_suggestions(self, category, **parameters):
        """Access the users in a given category of the suggested
           user list. It is recommended that end clients cache this data
           for no more than one hour.

        category -- The category to fetch users for.

        Returns: A list of user objects.
        """
        url = '1/users/suggestions/%s/members' % category
        return self.request('GET', url, parameters)

    def favorites(self, user=None, **parameters):
        """Returns the most recent favorite statuses for the
           authenticating user or a specified user by ID or screen name.

        user -- The screen name of ID of the user for whom to return results.

        Returns: A list of status objects.
        """
        if user:
            url = '1/favorites/%s' % user
        else:
            url = '1/favorites'
        return self.request('GET', url, parameters)

    def create_favorite(self, status, **parameters):
        """Favorites the specified status as the authenticating user.

        status -- The numerical ID of the status to favorite.

        Returns: A status object on success.
        """
        url = '1/favorites/create/%s' % status
        return self.request('POST', url, parameters)

    def destroy_favorite(self, status, **parameters):
        """Un-favorites the specified status as the authenticating user.

        status -- The numerical ID of the status to un-favorite.

        Returns: A status object on success.
        """
        url = '1/favorites/destroy/%s' % status
        return self.request('POST', url, parameters)

    def lists(self, user=None, **parameters):
        """Returns all lists that an user subscribes to, including
           their own.

        user -- The screen name of the user for whom to return results for.

        Returns: A list of list objects.
        """
        parameters['screen_name'] = user
        return self.request('GET', '1/lists/all', parameters)

    def list_timeline(self, owner=None, slug=None, **parameters):
        """Returns tweet timeline for members of the specified list.

        owner -- The screen name of the user who owns the list.
        slug -- The slug of the list to return timeline for.

        Returns: A list of status objects.
        """
        parameters.update({'slug': slug, 'owner_screen_name': owner})
        return self.request('GET', '1/lists/statuses', parameters)

    def list_add_member(self, owner=None, slug=None, member=None, **parameters):
        """Adds one or more members to a list. The authenticated user
           must own this list.

        owner -- The screen name of the user who owns the list.
        slug -- The slug of the list to add member(s) to.
        member -- The screen name of the user to add as a member of
                  the specified list. You may pass a list of screen names
                  to add multiple members with one request.

        Returns: A list object.
        """
        if isinstance(member, list):
            member = ','.join(member)
        parameters.update({'owner_screen_name': owner,
                           'slug': slug,
                           'screen_name': member})
        return self.request('POST', '1/lists/members/create_all', parameters)

    def list_remove_member(self, owner=None, slug=None, member=None, **parameters):
        """Removes the specified member from the list. List must be owned
           by the authenticating user.

        owner -- The screen name of the user whom owns the list.
        slug -- The slug of the list to remove the member from.
        member -- The screen name of the user to remove from list as a member.

        Returns: A list object.
        """
        parameters.update({'owner_screen_name': owner,
                           'slug': slug,
                           'screen_name': member})
        return self.request('POST', '1/lists/members/destroy', parameters)

    def list_memberships(self, user=None, **parameters):
        """Returns the lists the specified user has been added to. If no
           user is specified the authenticating user will be used.

        user -- The screen name of the user for whom to return results.

        Returns: A list of list objects.
        """
        parameters['screen_name'] = user
        return self.request('GET', '1/lists/memberships', parameters)

    def list_subscribers(self, owner=None, slug=None, **parameters):
        """Returns the subscribers of the specified list.

        owner -- The screen name of the user who owns the list.
        slug -- The slug of the list to return subscribers for.

        Returns: A list of user objects.
        """
        parameters.update({'owner_screen_name': owner,
                           'slug': slug})
        return self.request('GET', '1/lists/subscribers', parameters)

    def list_members(self, owner=None, slug=None, **parameters):
        """Returns the members of the specified list.

        owner -- The screen name of the user who owns the list.
        slug -- The slug of the list to return members for.

        Returns: A list of user objects.
        """
        parameters.update({'owner_screen_name': owner,
                           'slug': slug})
        return self.request('GET', '1/lists/members', parameters)

    def list_subscribe(self, owner=None, slug=None, **parameters):
        """Subscribes the authenticated user to the specified list.

        owner -- The screen name of the user who owns the list.
        slug -- The slug of the list to subscribe.

        Returns: A list object.
        """
        parameters.update({'owner_screen_name': owner,
                           'slug': slug})
        return self.request('POST', '1/lists/subscribers/create', parameters)

    def list_unsubscribe(self, owner=None, slug=None, **parameters):
        """Unsubscribes the authenticated user from the specified list.

        owner -- The screen name of the user who owns the list.
        slug -- The slug of the list to unsubscribe from.

        Returns: A list object.
        """
        parameters.update({'owner_screen_name': owner,
                           'slug': slug})
        return self.request('POST', '1/lists/subscribers/destroy', parameters)

    def list_destroy(self, owner=None, slug=None, **parameters):
        """Deletes the specified list. Authenticated user must own the list.

        owner -- The screen name of the user who owns the list.
        slug -- The slug of the list to be destroyed.

        Returns: A list object.
        """
        parameters.update({'owner_screen_name': owner,
                           'slug': slug})
        return self.request('POST', '1/lists/destroy', parameters)

    def list_create(self, name, description=None, mode=None, **parameters):
        """Creates a new list for the authenticated user.

        name -- The name for the list.
        description -- The description to give the list.
        mode -- Whether your list is public or private. (Default: public)

        Returns: A list object.
        """
        parameters.update({'name': name,
                           'description': description,
                           'mode': mode})
        return self.request('POST', '1/lists/create', parameters)

    def list_update(self, owner=None, slug=None, **parameters):
        """Updates the specified list. Authenticated user must own this list.

        owner -- The screen name of the user who owns the list.
        slug -- The slug of the list to update.

        Returns: A list object.
        """
        parameters.update({'owner_screen_name': owner,
                           'slug': slug})
        return self.request('POST', '1/lists/update', parameters)

    def list_show(self, owner=None, slug=None, **parameters):
        """Returns the specified list.

        owner -- The screen name of the user who owns the list.
        slug -- The slug of the list to return.

        Returns: A list object.
        """
        parameters.update({'owner_screen_name': owner,
                           'slug': slug})
        return self.request('GET', '1/lists/show', parameters)

    def list_subscriptions(self, user=None, **parameters):
        """Returns a collection of lists the specified user subscribes to.
           Does not include the user's own lists.

        user -- The screen name of the user for whom to return results for.

        Returns: A list of list objects.
        """
        parameters['screen_name'] = user
        return self.request('GET', '1/lists/subscriptions', parameters)

    def rate_limit_status(self):
        """Returns the remaining number of API requests available to the
           requesting user (if authenticated) or the IP address.

        Returns: A dict containing rate limit info.
        """
        return self.request('GET', '1/account/rate_limit_status')

    def verify_credentials(self):
        """Verify user credentials are valid by performing
           a request with authentication returning information about
           the authenticated user.

        Returns: An user object if successful, otherwise throws exception.
        """
        return self.request('GET', '1/account/verify_credentials')

    def update_profile(self, **parameters):
        """Sets values that users are able to set under the "Account" tab
           on their settings page. Only the parameters specified will
           be updated.

        See Twitter API documentation for supported parameters.

        Returns: A dict containing profile settings.
        """
        return self.request('POST', '1/account/update_profile', parameters)

    def update_profile_background(self, image=None, **parameters):
        """Updates the authenticating user's profile background image.
           This method can also be used to enable or disable the
           profile background image.

        image -- (optional) A path to a file or a tuple with format:
                   (filename, file-like-object)

        Returns: A dict containing profile settings.
        """
        if isinstance(image, str):
            image = (image, open(image, 'rb'))
        return self.request('POST',
                            '1/account/update_profile_background_image',
                            parameters,
                            files={'image': image} if image else None)

    def update_profile_colors(self, **parameters):
        """Sets one or more values that control the color scheme
           of the authenticating user's profile page.

        See Twitter API documentation for supported parameters.

        Returns: A dict containing profile settings.
        """
        return self.request('POST', '1/account/update_profile_colors', parameters)

    def update_profile_image(self, image, **parameters):
        """Updates the authenticating user's profile image.

        image -- (optional) A path to a file or a tuple with format:
                   (filename, file-like-object)

        Returns: A dict containing profile settings.
        """
        if isinstance(image, str):
            image = (image, open(image, 'rb'))
        return self.request('POST',
                            '1/account/update_profile_image',
                            parameters,
                            files={'image': image} if image else None)

    def saved_searches(self):
        """Returns the authenticated user's saved search queries.

        Returns: A list of saved searches.
        """
        return self.request('GET', '1/saved_searches')

    def saved_search_show(self, ID):
        """Returns the information for the saved search represented
           by the given ID. The authenticated user must own the saved search.

        ID -- The ID of the saved search to return.

        Returns: A saved search.
        """
        return self.request('GET', '1/saved_searches/show/%s' % ID)

    def saved_search_create(self, query, **parameters):
        """Creates a new saved search for the authenticated user.

        query -- The query of the search the user would like to save.

        Returns: A saved search.
        """
        parameters['query'] = query
        return self.request('POST', '1/saved_searches/create', parameters)

    def saved_search_destroy(self, ID):
        """Destroys a saved search for the authenticating user.

        ID -- The ID of the saved search to delete.

        Returns: A saved search.
        """
        return self.request('POST', '1/saved_searches/destroy/%s' % ID)

