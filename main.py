# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable
# law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and
# limitations under the License.

import jinja2
import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class ProvideURL(webapp2.RequestHandler):
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'),
                                      autoescape=True)
    index_template = template_env.get_template('index.html')

    def get(self):
        """Renders a page with a signed url for upload to a bucket with a CORs
        file."""
        upload_url = blobstore.create_upload_url(
            '/upload',
            gs_bucket_name='gcs-file-upload-demo')
        index_page = self.index_template.render({'upload_url': upload_url})
        self.response.write(index_page)
        return


class SuccessHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        self.response.headers.add('Access-Control-Allow-Origin', '*')

app = webapp2.WSGIApplication(
    [('/provideurl', ProvideURL),
     ('/upload', SuccessHandler)], debug=True)
