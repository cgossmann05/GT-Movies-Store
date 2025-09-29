from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MovieRequest, Petition, PetitionVote
from .forms import PetitionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# movies = [
#     {
#         'id': 1, 'name': 'Inception', 'price': 12, 'description': 'A mind-bending heist thriller.'
#     },
#     {
#         'id': 2, 'name': 'Avatar', 'price': 13, 'description': 'A journey to a distant world and the battle for resources.'
#     },
#     {
#         'id': 3, 'name': 'The Dark Knight', 'price': 14, 'description': 'Gothams vigilante faces the Joker.'
#     },
#     {
#         'id': 4, 'name': 'Titanic', 'price': 11, 'description': 'A love story set against the backdrop of the sinking Titanic.',
#     },
# ]

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = Movie.objects.all()
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def movie_requests(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if name and description:
            movie_request = MovieRequest()
            movie_request.name = name
            movie_request.description = description
            movie_request.user = request.user
            movie_request.save()
            return redirect('movies.requests')

    # Get user's movie requests
    user_requests = MovieRequest.objects.filter(user=request.user).order_by('-date_requested')

    template_data = {}
    template_data['title'] = 'Movie Requests'
    template_data['user_requests'] = user_requests
    return render(request, 'movies/requests.html', {'template_data': template_data})

@login_required
def delete_request(request, request_id):
    movie_request = get_object_or_404(MovieRequest, id=request_id, user=request.user)
    movie_request.delete()
    return redirect('movies.requests')

@login_required
def petition_list(request):
    petitions = Petition.objects.filter(status='active').order_by('-created_at')
    user_voted_petitions = set(
        PetitionVote.objects.filter(user=request.user).values_list('petition_id', flat=True)
    )
    template_data = {
        'title': 'Movie Petitions',
        'petitions': petitions
    }
    return render(request, 'movies/petition_list.html', {
        'template_data': template_data,
        'user_voted_petitions': user_voted_petitions
    })

@login_required
def petition_create(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('movies.petition_list')
    else:
        form = PetitionForm()

    template_data = {
        'title': 'Create Movie Petition',
        'form': form
    }
    return render(request, 'movies/petition_create.html', {'template_data': template_data})

@login_required
def petition_vote(request, pk):
    if request.method == 'POST':
        petition = get_object_or_404(Petition, pk=pk, status='active')
        vote_value = request.POST.get('vote')

        if vote_value not in ['yes', 'no']:
            messages.error(request, 'Invalid vote.')
            return redirect('movies.petition_list')

        vote_boolean = vote_value == 'yes'

        try:
            existing_vote = PetitionVote.objects.get(petition=petition, user=request.user)
            existing_vote.vote = vote_boolean
            existing_vote.save()
            messages.success(request, 'Your vote has been updated.')
        except PetitionVote.DoesNotExist:
            PetitionVote.objects.create(
                petition=petition,
                user=request.user,
                vote=vote_boolean
            )
            messages.success(request, 'Your vote has been recorded.')

    return redirect('movies.petition_list')