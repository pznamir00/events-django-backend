<h1>Events Django Application<h1>
<hr/>
<div>
    <h3>Description</h3>
    <p>
        Events-Django-App is an application that provides a database of events in the user's area. Application is splited for3 parts: core, users and tickets.<br/>
        <b>Core</b> part provides the events catalog and related models for user. Addltionally has a system of sending emails to users with Celery.<br/>
        <b>Users</b> includes a authorization system and extends default Django User model.<br/>
        <b>Tickets</b> is very easy selling tickets system. By default events are free for everybody but there is an option to set 'is_free'=False. Then user has to provides a ticket file that will be selling for clients. That part generates a new ticket with unique QR code and send it to user's email.
    </p>
</div>
<hr/>
<div>
    <h3>Technology Stack</h3>
    <ul>
        <li>Django</li>
        <li>Django-Rest-Framework</li>
        <li>Postgres</li>
        <li>Postgis</li>
        <li>Docker</li>
        <li>Docker-compose</li>
        <li>Celery</li>
    </ul>
</div>
<hr/>
<div>
    <h3>Endpoints</h3>
    <ul>
        <li>
            Core (prefix: /api/core/)
            <ul>
                <li>
                    <b>CRUD categories/</b> - crud for category model; write only for admin
                    <p>Fields: [name]</p>    
                </li>
                <li>
                    <b>GET, POST, DELETE followed-hashtags/</b> - handling of followed hashtags for user (required authorization)
                    <p>Fields: [value]</p>
                </li>
                <li>
                    <b>GET own-events/</b> - list of own events (required authorization)
                </li>
                <li>
                    <b>CRUD events/</b> - CRUD for event model
                    <ul>
                        <li>
                            GET - list
                            <br/>
                            <p>Filter params: [range, latitude, longitude, keywords, created_at, updated_at, event_datetime, category, promoter, is_free]</p>
                        </li>
                        <li>GET {id}/ - retrieve</li>
                        <li>
                            POST create - (required authorization)
                            <p>Fields: [title, description, event_datetime, location, category{ latitude, longitude }]</p>
                        </li>
                        <li>
                            PATCH {id}/ - update (required authorization as owner)
                            <p>Fields: [title, description, event_datetime, location, category{ latitude, longitude }, took_place, is_free, is_private, canceled]</p>
                            <br/>
                            <p>If user passes a is_free=False, has to provides ticket{ template(pdf file), quantity } field also</p>
                        </li>
                        <li>DELETE {id}/ - destroy (required authorization as owner)</li>
                    </ul>
                </li>
            </ul>    
        </li>
        <li>
            Users (prefix: /api/users/)
            <ul>
                <li><b><a href="https://dj-rest-auth.readthedocs.io/en/latest/">dj-rest-auth routes</a></b></li>
                <li><b>GET user/</b> - get user's data</li>
                <li>
                    <b>PATCH user/</b> - update user's data
                    <p>Fields: [phone_number, country, state, city, street, home_nb, zip_code, avatar]</p>
                </li>
                <li>
                    <b>POST register/</b> - register new user
                    <p>Fields: [email, username, password1, password2, phone_number, country, state, city, street, home_nb, zip_code]</p>
                </li>
            </ul>   
        </li>
        <li>
            Tickets (prefix: /api/tickets/)
            <ul>
                <li>
                    <b>POST events/{event_id}/tickets/</b> - get ticket of event (in this version, in production should returns after payment)
                    <p>Fields: []</p>
                </li>
                <li><b>GET events/{event_id}/tickets/{ticket_id}/'</b> - validate if ticket does exist and is not used. (requires event's owner logged)</li>
            </ul>
        </li>
    </ul>
</div>