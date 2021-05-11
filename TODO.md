# TODOs

## backend
- [low priority] emails should be unique
- - default django user model allows duplicate emails
- - will cause problems if we do user lookup by email
- [low priority] custom filename for media uploads to prevent path collision
- - if two files with same filename are uploaded, the first one keeps its original name, the second one will have a random string appended to it (current behavior)
- - for example, two files named `paper.pdf` would be saved as `paper.pdf` and `paper_j3mHTpk.pdf`
- - the username of the submmitting user gets prepended to each uploaded file (desired behavior)
- - in this case the two identically named files would be saved as `user1-paper.pdf` and `user2-paper.pdf`
- - maybe add conference id as well
- [low priority] custom serializer for password reset confirm
- - the default email template contains a link pointing to `https://se-placeholder.cf/password/reset/confirm/<slug:uidb64>/<slug:token>`
- - should be configured to link to `https://se-placeholder.cf/recover-password.html?id=<uidb64>&token=<token>` which will make the request to the api

## frontend
- [medium priority] disable `get a ticket` button for conferences that the user already joined
- [medium priority] make tag inputs more intuitive
- [medium priority] also update application state on the frontend
- - when the application state changes (the user creates a new conference, for example) the window reloads (current behavior)
- - update the components on state change, without reloading
- [low priority] show `no papers submitted` when viewing paper list for a conferene with no submissions
- [low priority] paper list modal needs bottom margin
- [low priority] popup box for info and error messages
- - currently tag inputs look the same way as text inuts
- - for tag inputs the user has to press enter to add the input text to the tag list
- [low priority] do not hardcode server url in paper downloads
- - `<a :href="'http://kind-wind-83282.pktriot.net' + paper.abstract">`