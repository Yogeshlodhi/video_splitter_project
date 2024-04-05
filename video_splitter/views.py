from django.shortcuts import render
from django.http import HttpResponse
from .forms import VideoSplitForm
import ffmpeg
import os

def split_video(input_video_path, output_dir, num_parts):
    input_video = ffmpeg.input(input_video_path)
    duration = float(ffmpeg.probe(input_video_path)['format']['duration'])
    part_duration = duration / num_parts
    for i in range(num_parts):
        output_path = os.path.join(output_dir, f'part_{i+1}.mp4')
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
            return HttpResponse('Video successfully split!')
    else:
        form = VideoSplitForm()
    return render(request, 'video_splitter/home.html', {'form': form})



