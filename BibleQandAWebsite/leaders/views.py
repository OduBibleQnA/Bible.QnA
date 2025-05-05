from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from os import getenv
# Local
from form.models import Question, Testimony
from form.utils.encryption import decrypt_contact_detail
from .auth import get_credentials_from_session, get_youtube_flow, store_credentials_in_session
from .decorators import staff_and_group_required
from .forms import QuestionStaffForm

@staff_and_group_required("podcasters")
def youtube_oauth2callback(request):
    flow = get_youtube_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    creds = flow.credentials

    # Fetch user's email
    import requests
    userinfo_response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {creds.token}"},
    )
    user_info = userinfo_response.json()
    email = user_info.get("email")

    # Restrict access to specific email
    if email != getenv('GOOGLE_OATH_ALLOWED_EMAIL'):
        messages.error(request, "Access denied: unauthorized Google account.")
        return redirect("leaders:youtube:youtube_auth_start")

    store_credentials_in_session(request.session, creds)
    return redirect('leaders:youtube:youtube_dashboard')


@staff_and_group_required("podcasters")
def youtube_dashboard(request):
    creds = get_credentials_from_session(request.session)
    if not creds or not creds.valid:
        return redirect("leaders:youtube:youtube_auth_start")

    youtube = build("youtube", "v3", credentials=creds)

    # Get channel info (title + subscriber count)
    channel_response = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        mine=True
    ).execute()

    channel = channel_response["items"][0]
    title = channel["snippet"]["title"]
    subscriber_count = int(channel["statistics"].get("subscriberCount", 0))
    uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    # Get all uploaded video IDs
    video_ids = []
    next_page_token = None
    while True:
        playlist_items = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        video_ids += [item["contentDetails"]["videoId"] for item in playlist_items["items"]]
        next_page_token = playlist_items.get("nextPageToken")
        if not next_page_token:
            break

    # Sum view counts from all videos
    total_views = 0
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        video_response = youtube.videos().list(
            part="statistics",
            id=",".join(batch_ids)
        ).execute()

        for item in video_response["items"]:
            total_views += int(item["statistics"].get("viewCount", 0))

    return render(request, "leaders/youtube/dashboard.html", {
        "title": title,
        "stats": {
            "viewCount": total_views,
            "videoCount": len(video_ids),
            "subscriberCount": subscriber_count
        }
    })



@staff_and_group_required("podcasters")
def youtube_analytics(request):
    creds = get_credentials_from_session(request.session)
    if not creds or not creds.valid:
        return redirect("leaders:youtube:youtube_auth_start")

    youtube = build("youtube", "v3", credentials=creds)

    video_ids = []
    next_page_token = None

    while True:
        search_response = youtube.search().list(
            part="id",
            forMine=True,
            type="video",
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        video_ids += [item["id"]["videoId"] for item in search_response.get("items", [])]
        next_page_token = search_response.get("nextPageToken")
        if not next_page_token:
            break

    videos = []
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        video_response = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(batch_ids)
        ).execute()
        for item in video_response.get("items", []):
            # Convert publishedAt to datetime
            published_at = item["snippet"].get("publishedAt")
            print(published_at)
            if published_at:
                try:
                    item["snippet"]["published_datetime"] = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                except ValueError:
                    item["snippet"]["published_datetime"] = None
            videos.append(item)

    return render(request, "leaders/youtube/analytics.html", {"videos": videos})


@staff_and_group_required("podcasters")
def youtube_upload(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        hashtags = request.POST.get("hashtags", "")
        video_file = request.FILES.get("video")
        thumbnail_file = request.FILES.get("thumbnail")

        if not (title and description and video_file and thumbnail_file):
            messages.error(request, "All fields including thumbnail are required.")
            return redirect("leaders:youtube:youtube_upload")

        # Append hashtags to the description
        if hashtags:
            hashtag_list = [tag.strip() for tag in hashtags.split("#") if tag.strip()]
            formatted_hashtags = " ".join(f"#{tag}" for tag in hashtag_list)
            description = f"{description}\n\n{formatted_hashtags}"

        # Save files temporarily
        temp_video_path = settings.TEMP_DIR / video_file.name
        with temp_video_path.open("wb+") as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        temp_thumbnail_path = settings.TEMP_DIR / thumbnail_file.name
        with temp_thumbnail_path.open("wb+") as f:
            for chunk in thumbnail_file.chunks():
                f.write(chunk)

        creds = get_credentials_from_session(request.session)
        if not creds or not creds.valid:
            return redirect("leaders:youtube:youtube_auth_start")

        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {
                "title": title,
                "description": description,
            },
            "status": {
                "privacyStatus": "public",
            },
            "contentDetails": {
                "madeForKids": False,
            }
        }

        media = MediaFileUpload(str(temp_video_path), chunksize=-1, resumable=True, mimetype="video/*")

        try:
            upload_response = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            ).execute()

            video_id = upload_response["id"]

            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(temp_thumbnail_path), mimetype="image/*")
            ).execute()

            messages.success(request, f"Video uploaded successfully! ID: {video_id}")
        except Exception as e:
            messages.error(request, f"Upload failed: {e}")
        finally:
            temp_video_path.unlink(missing_ok=True)
            temp_thumbnail_path.unlink(missing_ok=True)

        return redirect("leaders:youtube:youtube_dashboard")

    return render(request, "leaders/youtube/upload.html")




@staff_and_group_required("podcasters")
def spotify_redirect(request):
    return redirect("https://creators.spotify.com/pod/dashboard/episode/wizard/")

@staff_and_group_required("podcasters")
def start_auth(request):
    flow = get_youtube_flow()
    auth_url, _ = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        include_granted_scopes="true"
    )
    return redirect(auth_url)

@staff_and_group_required("podcasters")
def oauth2_callback(request):
    flow = get_youtube_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    store_credentials_in_session(request.session, credentials)
    request.session["google_credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    return redirect("leaders:youtube:youtube_dashboard")

def get_authenticated_service(session):
    creds_data = get_credentials_from_session(session)
    if not creds_data:
        return None

    creds = Credentials(**creds_data)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        store_credentials_in_session(session, creds)
    return creds

@staff_member_required
def view_questions(request):
    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")
    answer_filter = request.GET.get("filter", "")

    questions = Question.objects.filter(archived=False)

    if search_query:
        questions = questions.filter(question__icontains=search_query)

    if status_filter == "pending":
        questions = questions.filter(answer_date__isnull=True)
    elif status_filter == "scheduled":
        questions = questions.filter(answer_date__isnull=False)

    if answer_filter == "unanswered":
        questions = questions.filter(answered=False)
    elif answer_filter == "marked":
        questions = questions.filter(marked=True)

    # Sort: unanswered first
    questions = questions.order_by('answered', 'answer_date')

    return render(request, 'leaders/questions/view_questions.html', {
        'questions': questions,
        'search_query': search_query,
        'status_filter': status_filter
    })




@staff_member_required
def mark_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        form = QuestionStaffForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('leaders:core:view_questions')
    else:
        form = QuestionStaffForm(instance=question)

    return render(request, 'leaders/questions/mark_question.html', {'form': form, 'question': question})


@staff_member_required
def archived_questions(request):
    if request.method == "POST":
        ids_to_delete = request.POST.getlist("delete_ids")
        if ids_to_delete:
            Question.objects.filter(id__in=ids_to_delete).delete()
            messages.success(request, f"Deleted {len(ids_to_delete)} archived question(s).")
            return redirect("leaders:core:archived_questions")

    questions = Question.objects.filter(archived=True)
    return render(request, "leaders/questions/archived_questions.html", {"questions": questions})

@staff_member_required
def unarchive_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.archived = False
    question.save()
    return redirect('leaders:archived_questions')


@staff_and_group_required("podcasters")
def pending_testimonies(request):
    search_query = request.GET.get('search', '').strip()
    testimonies = Testimony.objects.filter(archived=False)

    if search_query:
        testimonies = testimonies.filter(shortened_testimony__icontains=search_query)

    for t in testimonies:
        t.decrypted_contact = decrypt_contact_detail(t.encrypted_contact_detail)

    return render(request, 'leaders/podcasts/testimonies_pending.html', {
        'testimonies': testimonies,
        'search_query': search_query,
    })


@staff_and_group_required("podcasters")
def approve_testimony(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    testimony.approved = True
    testimony.save()
    return redirect('leaders:podcast:testimonies_pending')

@staff_and_group_required("podcasters")
def archive_testimony(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    testimony.archived = True
    testimony.save()
    return redirect('leaders:podcast:testimonies_pending')

@staff_and_group_required("podcasters")
def delete_testimony(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    testimony.delete()
    return redirect('leaders:podcast:archived_testimonies')

@staff_and_group_required("podcasters")
def archived_testimonies(request):
    search_query = request.GET.get('search', '').strip()
    testimonies = Testimony.objects.filter(archived=True)

    if search_query:
        testimonies = testimonies.filter(shortened_testimony__icontains=search_query)

    for t in testimonies:
        t.decrypted_contact = decrypt_contact_detail(t.encrypted_contact_detail)

    return render(request, 'leaders/podcasts/testimonies_archived.html', {
        'testimonies': testimonies,
        'search_query': search_query,
    })


@staff_member_required
def unarchive_testimony(request, pk):
    testimony = get_object_or_404(Testimony, pk=pk)
    testimony.archived = False
    if(testimony.approved): testimony.approved = False
    testimony.save()
    return redirect('leaders:podcast:archived_testimonies')

