from django.test import TestCase
from django.urls import reverse
from .models import Video
# Create your tests here.

class TestHomePageMessage(TestCase):

    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Sports Videos')


class TestAddVideos(TestCase):

    def test_add_video(self):

        valid_video = {
            'name': 'yoga',
            'url': 'https://www.youtube.com/watch?v=4vTJHUDB5ak',
            'notes': 'yoga for neck and shoulders'
        }

        url = response('add_video')
        
        # follow=True necessary because the view redirects to the video list after a video is successfully added.
        response = self.client.post(add_video, data=valid_video, follow=True)

        # redirect to video list 
        self.assertTemplateUsed('video_collection/video_list.html')

        # video list shows new video 
        self.assertContains(response, 'yoga')
        self.assertContains(response, 'https://www.youtube.com/watch?v=4vTJHUDB5ak')
        self.assertContains(response, 'yoga for neck and shoulders')

        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        video = Video.objects.first()

        self.assertEqual('yoga', video.name)
        self.assertEqual('https://www.youtube.com/watch?v=4vTJHUDB5ak', video.url)
        self.assertEqual('yoga for neck and shoulders', video.notes)
        self.assertEqual('4vTJHUDB5ak', video.video_id)



    def test_add_video_invalid_url_not_added(self):

            invalid_video_urls = [
                'https://www.youtube.com/watch',
                'https://www.youtube.com/watch?',
                'https://github.com',
                'https://www.youtube.com/watch?v=',
                'https://minneapolis.edu'
                'https://minneapolis.edu?v=123456'
            ]

            for invalid_url in invalid_video_urls:

                new_video = {
                    'name': 'example',
                    'url': invalid_url,
                    'notes': 'exmaple notes'
                }

                url = reverse('add_video')
                response = self.client.post(url, new_video)
                self.assertTemplateNotUsed('video_collection/add.html')

                messages = response.context['messages']
                message_texts = [ message.message for message in messages ]

                self.assertIn('Invalid YouTube URL', messages_texts)
                self.assertIn('Please check the data entered', messages_texts)

                video_count = Video.objects.count()
                self.assertEqual(0, video_count)





class TestVideoList(TestCase):

    def test_all_videos_displayed_in_correct_order(self):

        v1 = Video.objects.create(name='fgc', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='ABC', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(name='por', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=126')

        expected_video_order = [v2, v4, v3, v1]

        url = reverse('video_list')
        response = self.client.get(reverse('video_list'))

        videos_in_template = list(response.context['videos'])

        self.assertEqual(videos_in_template, expected_video_order)
