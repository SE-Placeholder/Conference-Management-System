from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ConferenceListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response([
            {
                'name': 'YeetConf 2021',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur commodo leo sit amet neque tristique accumsan. Cras quis feugiat nisl, ut interdum quam. Phasellus quis tortor eu sem placerat hendrerit. Aliquam a egestas massa, id pellentesque libero. Pellentesque semper lectus eget magna lacinia pellentesque. Maecenas at bibendum libero. Etiam urna purus, bibendum eu augue ac, pharetra luctus turpis. Vivamus maximus nisl eleifend neque cursus, sit amet mollis lorem laoreet. Nulla eu arcu ultricies, suscipit nisi a, egestas elit. Aenean finibus lectus sit amet mi convallis elementum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Morbi vel metus ornare, vehicula turpis vitae, finibus lorem. Donec ultricies ultrices mauris, eu fermentum ex accumsan ac. Quisque sit amet massa at tellus sodales ultricies sed et mi. Mauris viverra dictum neque nec placerat.',
                'deadline': '2021/05/10'
            },
            {
                'name': 'YeetConf 2021',
                'description': 'Donec suscipit, mi non aliquet commodo, diam lacus pharetra nisl, quis congue nibh dui in est. Phasellus quis dignissim lectus. Morbi vitae dui mollis, blandit risus sit amet, sodales mauris. Duis pellentesque nibh ut dolor mattis, id consequat tellus tristique. Aliquam erat volutpat. Donec efficitur tincidunt turpis, quis pharetra augue auctor ut. Pellentesque et elit interdum, consectetur lorem in, iaculis neque. In tristique, justo eget elementum finibus, sapien neque faucibus ligula, ut pretium urna nulla non sem. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Mauris mollis fringilla sem vel cursus. Nunc efficitur sollicitudin gravida. Morbi eu ante a purus aliquam faucibus. Donec venenatis ipsum mauris. In sed rutrum eros, id sodales lectus. Cras lobortis nisl sit amet porta ultricies.',
                'deadline': '2021/05/10'
            },
            {
                'name': 'YeetConf 2021',
                'description': 'Proin a porttitor erat. Proin bibendum sapien nec quam fermentum, in pretium magna efficitur. Morbi in neque dui. Quisque et odio efficitur, vehicula velit ut, lobortis nunc. Aliquam posuere sit amet dolor id dignissim. Praesent quis maximus orci. Integer aliquet auctor urna, sed luctus velit scelerisque maximus. Sed in ipsum ex. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum at dolor lacus. Aenean malesuada auctor lacus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vestibulum libero est, in rhoncus turpis pharetra ut. Integer aliquet ex nec lectus laoreet malesuada. Quisque eu lorem auctor, convallis justo ac, bibendum diam.',
                'deadline': '2021/05/10'
            }
        ])


class RestrictedConferenceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response([
            {
                'name': 'YeetConf 2021',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur commodo leo sit amet neque tristique accumsan. Cras quis feugiat nisl, ut interdum quam. Phasellus quis tortor eu sem placerat hendrerit. Aliquam a egestas massa, id pellentesque libero. Pellentesque semper lectus eget magna lacinia pellentesque. Maecenas at bibendum libero. Etiam urna purus, bibendum eu augue ac, pharetra luctus turpis. Vivamus maximus nisl eleifend neque cursus, sit amet mollis lorem laoreet. Nulla eu arcu ultricies, suscipit nisi a, egestas elit. Aenean finibus lectus sit amet mi convallis elementum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Morbi vel metus ornare, vehicula turpis vitae, finibus lorem. Donec ultricies ultrices mauris, eu fermentum ex accumsan ac. Quisque sit amet massa at tellus sodales ultricies sed et mi. Mauris viverra dictum neque nec placerat.',
                'deadline': '2021/05/10'
            },
            {
                'name': 'YeetConf 2021',
                'description': 'Donec suscipit, mi non aliquet commodo, diam lacus pharetra nisl, quis congue nibh dui in est. Phasellus quis dignissim lectus. Morbi vitae dui mollis, blandit risus sit amet, sodales mauris. Duis pellentesque nibh ut dolor mattis, id consequat tellus tristique. Aliquam erat volutpat. Donec efficitur tincidunt turpis, quis pharetra augue auctor ut. Pellentesque et elit interdum, consectetur lorem in, iaculis neque. In tristique, justo eget elementum finibus, sapien neque faucibus ligula, ut pretium urna nulla non sem. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Mauris mollis fringilla sem vel cursus. Nunc efficitur sollicitudin gravida. Morbi eu ante a purus aliquam faucibus. Donec venenatis ipsum mauris. In sed rutrum eros, id sodales lectus. Cras lobortis nisl sit amet porta ultricies.',
                'deadline': '2021/05/10'
            },
            {
                'name': 'YeetConf 2021',
                'description': 'Proin a porttitor erat. Proin bibendum sapien nec quam fermentum, in pretium magna efficitur. Morbi in neque dui. Quisque et odio efficitur, vehicula velit ut, lobortis nunc. Aliquam posuere sit amet dolor id dignissim. Praesent quis maximus orci. Integer aliquet auctor urna, sed luctus velit scelerisque maximus. Sed in ipsum ex. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum at dolor lacus. Aenean malesuada auctor lacus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vestibulum libero est, in rhoncus turpis pharetra ut. Integer aliquet ex nec lectus laoreet malesuada. Quisque eu lorem auctor, convallis justo ac, bibendum diam.',
                'deadline': '2021/05/10'
            }
        ])
