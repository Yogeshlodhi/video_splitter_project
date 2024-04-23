# from django.shortcuts import render
# from django.http import HttpResponse
# from .forms import VideoSplitForm
# import ffmpeg
# import os

# def split_video(input_video_path, output_dir, num_parts):
#     input_video = ffmpeg.input(input_video_path)
#     duration = float(ffmpeg.probe(input_video_path)['format']['duration'])
#     part_duration = duration / num_parts
#     for i in range(num_parts):
#         output_path = os.path.join(output_dir, f'part_{i+1}.mp4')
#         ffmpeg.output(input_video, output_path, ss=i*part_duration, t=part_duration).run()

# def home(request):
#     if request.method == 'POST':
#         form = VideoSplitForm(request.POST, request.FILES)
#         if form.is_valid():
#             video = request.FILES['video']
#             num_parts = form.cleaned_data['num_parts']
#             output_dir = 'media/output'
#             os.makedirs(output_dir, exist_ok=True)
#             video_path = os.path.join('media', video.name)
#             with open(video_path, 'wb') as f:
#                 for chunk in video.chunks():
#                     f.write(chunk)
#             split_video(video_path, output_dir, num_parts)
#             # return HttpResponse('Video successfully split!')
#             return render(request, 'video_splitter/success_message.html')
#     else:
#         form = VideoSplitForm()
#     return render(request, 'video_splitter/home.html', {'form': form})



from django.shortcuts import render
from django.http import HttpResponse
from .forms import VideoSplitForm
import ffmpeg
import os


import datetime

def split_video(input_video_path, output_dir, num_parts):
    input_video = ffmpeg.input(input_video_path)
    duration = float(ffmpeg.probe(input_video_path)['format']['duration'])
    part_duration = duration / num_parts
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    for i in range(num_parts):
        output_filename = f'{current_time}_part_{i+1}.mp4'  # Unique filename based on current date/time and part number
        output_path = os.path.join(output_dir, output_filename)
        ffmpeg.output(input_video, output_path, ss=i*part_duration, t=part_duration).run()

def home(request):
    if request.method == 'POST':
        form = VideoSplitForm(request.POST, request.FILES)
        if form.is_valid():
            video = request.FILES['video']
            num_parts = form.cleaned_data['num_parts']
            output_dir = 'media/output'
            os.makedirs(output_dir, exist_ok=True)
            video_path = os.path.join('media', video.name)
            with open(video_path, 'wb') as f:
                for chunk in video.chunks():
                    f.write(chunk)
            split_video(video_path, output_dir, num_parts)
            # Get paths of split videos
            split_videos = {}
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            for i in range(num_parts):
                output_filename = f'{current_time}_part_{i+1}.mp4'
                split_videos[i + 1] = os.path.join(output_dir, output_filename)
            return render(request, 'video_splitter/success_message.html', {'split_videos': split_videos})
    else:
        form = VideoSplitForm()
    return render(request, 'video_splitter/home.html', {'form': form})


# def split_video(input_video_path, output_dir, num_parts):
#     input_video = ffmpeg.input(input_video_path)
#     duration = float(ffmpeg.probe(input_video_path)['format']['duration'])
#     part_duration = duration / num_parts
#     for i in range(num_parts):
#         output_path = os.path.join(output_dir, f'part_{i+1}.mp4')
#         ffmpeg.output(input_video, output_path, ss=i*part_duration, t=part_duration).run()

# def home(request):
#     if request.method == 'POST':
#         form = VideoSplitForm(request.POST, request.FILES)
#         if form.is_valid():
#             video = request.FILES['video']
#             num_parts = form.cleaned_data['num_parts']
#             output_dir = 'media/output'
#             os.makedirs(output_dir, exist_ok=True)
#             video_path = os.path.join('media', video.name)
#             with open(video_path, 'wb') as f:
#                 for chunk in video.chunks():
#                     f.write(chunk)
#             split_video(video_path, output_dir, num_parts)
#             # Get paths of split videos
#             split_videos = {i + 1: os.path.join(output_dir, f'part_{i+1}.mp4') for i in range(num_parts)}
#             return render(request, 'video_splitter/success_message.html', {'split_videos': split_videos})
#     else:
#         form = VideoSplitForm()
#     return render(request, 'video_splitter/home.html', {'form': form})



