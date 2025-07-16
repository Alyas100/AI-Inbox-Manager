from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id='555750767356-olt7uoudaj1v4jfs42a8i6p8r9m1m0r9.apps.googleusercontent.com',
    client_secret='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',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile https://www.googleapis.com/auth/gmail.readonly'
        
    }
)