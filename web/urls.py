from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from . import admin_views, peer_challenge_views, quiz_views, views
from .views import (
    GoodsListingView,
    GradeableLinkCreateView,
    GradeableLinkDetailView,
    GradeableLinkListView,
    add_goods_to_cart,
    grade_link,
    sales_analytics,
    sales_data,
    streak_detail,
)

# Non-prefixed URLs
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # Language selection URLs
    path("captcha/", include("captcha.urls")),  # CAPTCHA URLs should not be language-prefixed
]

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))  # Browser reload URLs
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Add this line
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Language-prefixed URLs
urlpatterns += i18n_patterns(
    path("", views.index, name="index"),
    path("create-test-data/", views.run_create_test_data, name="create_test_data"),
    path("learn/", views.learn, name="learn"),
    path("teach/", views.teach, name="teach"),
    path("about/", views.about, name="about"),
    path("profile/<str:username>/", views.public_profile, name="public_profile"),
    path("graphing_calculator/", views.graphing_calculator, name="graphing_calculator"),
    path("certificate/<uuid:certificate_id>/", views.certificate_detail, name="certificate_detail"),
    path("certificate/generate/<int:enrollment_id>/", views.generate_certificate, name="generate_certificate"),
    path("donate/", views.donate, name="donate"),
    path("donate/payment-intent/", views.create_donation_payment_intent, name="create_donation_payment_intent"),
    path("donate/subscription/", views.create_donation_subscription, name="create_donation_subscription"),
    path("donate/success/", views.donation_success, name="donation_success"),
    path("donate/cancel/", views.donation_cancel, name="donation_cancel"),
    path("donate/webhook/", views.donation_webhook, name="donation_webhook"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/create/", views.create_blog_post, name="create_blog_post"),
    path("blog/tag/<str:tag>/", views.blog_tag, name="blog_tag"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    # Success Stories URLs
    path("success-stories/", views.success_story_list, name="success_story_list"),
    path("success-stories/create/", views.create_success_story, name="create_success_story"),
    path("success-stories/<slug:slug>/", views.success_story_detail, name="success_story_detail"),
    path("success-stories/<slug:slug>/edit/", views.edit_success_story, name="edit_success_story"),
    path("success-stories/<slug:slug>/delete/", views.delete_success_story, name="delete_success_story"),
    # Authentication URLs
    path("accounts/signup/", views.signup_view, name="account_signup"),  # Our custom signup view
    path("accounts/", include("allauth.urls")),
    path("profile/", views.profile, name="profile"),
    path("accounts/profile/", views.profile, name="accounts_profile"),
    # Dashboard URLs
    path("dashboard/student/", views.student_dashboard, name="student_dashboard"),
    path("dashboard/teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("dashboard/content/", views.content_dashboard, name="content_dashboard"),
    # Course Management
    path("courses/create/", views.create_course, name="create_course"),
    path("courses/search/", views.course_search, name="course_search"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("courses/<slug:course_slug>/enroll/", views.enroll_course, name="enroll_course"),
    path("courses/<slug:slug>/add-session/", views.add_session, name="add_session"),
    path("courses/<slug:slug>/edit/", views.update_course, name="update_course"),
    path("courses/<slug:slug>/toggle-status/", views.toggle_course_status, name="toggle_course_status"),
    path("sessions/<int:session_id>/edit/", views.edit_session, name="edit_session"),
    path("courses/<slug:slug>/add-review/", views.add_review, name="add_review"),
    path("courses/<slug:slug>/delete/", views.delete_course, name="delete_course"),
    path("courses/<slug:slug>/add-session/", views.add_session, name="add_session"),
    path("courses/<slug:slug>/confirm-rolled-sessions/", views.confirm_rolled_sessions, name="confirm_rolled_sessions"),
    path("courses/<slug:slug>/message-students/", views.message_enrolled_students, name="message_students"),
    path("courses/<slug:slug>/add-student/", views.add_student_to_course, name="add_student_to_course"),
    path("teachers/<int:teacher_id>/message/", views.message_teacher, name="message_teacher"),
    path("sessions/<int:session_id>/duplicate/", views.duplicate_session, name="duplicate_session"),
    # Payment URLs
    path(
        "courses/<slug:slug>/create-payment-intent/",
        views.create_payment_intent,
        name="create_payment_intent",
    ),
    path("stripe-webhook/", views.stripe_webhook, name="stripe_webhook"),
    # Admin and Utilities
    path("github_update/", views.github_update, name="github_update"),
    path(f"{settings.ADMIN_URL}/dashboard/", admin_views.admin_dashboard, name="admin_dashboard"),
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("subjects/", views.subjects, name="subjects"),
    # Progress tracking URLs
    path(
        "sessions/<int:session_id>/attendance/",
        views.mark_session_attendance,
        name="mark_session_attendance",
    ),
    path(
        "sessions/<int:session_id>/complete/",
        views.mark_session_completed,
        name="mark_session_completed",
    ),
    path(
        "enrollment/<int:enrollment_id>/progress/",
        views.student_progress,
        name="student_progress",
    ),
    path(
        "courses/<slug:slug>/progress/",
        views.course_progress_overview,
        name="course_progress_overview",
    ),
    path(
        "courses/<slug:slug>/materials/upload/",
        views.upload_material,
        name="upload_material",
    ),
    path(
        "courses/<slug:slug>/materials/<int:material_id>/delete/",
        views.delete_material,
        name="delete_material",
    ),
    path(
        "courses/<slug:slug>/materials/<int:material_id>/download/",
        views.download_material,
        name="download_material",
    ),
    path(
        "courses/<slug:slug>/marketing/",
        views.course_marketing,
        name="course_marketing",
    ),
    path(
        "courses/<slug:slug>/analytics/",
        views.course_analytics,
        name="course_analytics",
    ),
    path("calendar/feed/", views.calendar_feed, name="calendar_feed"),
    path(
        "calendar/session/<int:session_id>/",
        views.calendar_links,
        name="calendar_links",
    ),
    path("streak/", streak_detail, name="streak_detail"),
    # Forum URLs
    path("forum/", views.forum_categories, name="forum_categories"),
    path("forum/category/create/", views.create_forum_category, name="create_forum_category"),
    path("forum/category/<slug:slug>/", views.forum_category, name="forum_category"),
    path("forum/category/<slug:category_slug>/create/", views.create_topic, name="create_topic"),
    path(
        "forum/<slug:category_slug>/<int:topic_id>/",
        views.forum_topic,
        name="forum_topic",
    ),
    path("forum/topic/<int:topic_id>/edit/", views.edit_topic, name="edit_topic"),
    path("forum/sync-milestones/", views.sync_github_milestones, name="sync_github_milestones"),
    # Peer Networking URLs
    path("peers/", views.peer_connections, name="peer_connections"),
    path(
        "peers/connect/<int:user_id>/",
        views.send_connection_request,
        name="send_connection_request",
    ),
    path(
        "peers/handle/<int:connection_id>/<str:action>/",
        views.handle_connection_request,
        name="handle_connection_request",
    ),
    path("peers/messages/<int:user_id>/", views.peer_messages, name="peer_messages"),
    # Study Groups URLs
    path("courses/<int:course_id>/groups/", views.study_groups, name="study_groups"),
    path("groups/<int:group_id>/", views.study_group_detail, name="study_group_detail"),
    path("sessions/<int:session_id>/", views.session_detail, name="session_detail"),
    path("sitemap/", views.sitemap, name="sitemap"),
    # Cart URLs
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/course/<int:course_id>/", views.add_course_to_cart, name="add_course_to_cart"),
    path("cart/add/session/<int:session_id>/", views.add_session_to_cart, name="add_session_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/payment-intent/", views.create_cart_payment_intent, name="create_cart_payment_intent"),
    path("cart/checkout/success/", views.checkout_success, name="checkout_success"),
    path("markdownx/", include("markdownx.urls")),
    # Course Invitation URLs
    path("courses/<int:course_id>/invite/", views.invite_student, name="invite_student"),
    path("terms/", views.terms, name="terms"),
    path("feedback/", views.feedback, name="feedback"),
    path("stripe/connect/onboarding/", views.stripe_connect_onboarding, name="stripe_connect_onboarding"),
    path("stripe/connect/webhook/", views.stripe_connect_webhook, name="stripe_connect_webhook"),
    path("courses/<slug:slug>/calendar/", views.get_course_calendar, name="course_calendar"),
    # Calendar URLs
    path("calendar/create/", views.create_calendar, name="create_calendar"),
    path("calendar/<str:share_token>/", views.view_calendar, name="view_calendar"),
    path("calendar/<str:share_token>/add-slot", views.add_time_slot, name="add_time_slot"),
    path("calendar/<str:share_token>/remove-slot", views.remove_time_slot, name="remove_time_slot"),
    path("calendar/<str:share_token>/data", views.get_calendar_data, name="get_calendar_data"),
    path("status/", views.system_status, name="system_status"),
    # Challenge URLs
    path("challenges/<int:week_number>/", views.challenge_detail, name="challenge_detail"),
    path("challenges/<int:week_number>/submit/", views.challenge_submit, name="challenge_submit"),
    path("current-weekly-challenge/", views.current_weekly_challenge, name="current_weekly_challenge"),
    # Educational Videos URLs
    path("fetch-video-title/", views.fetch_video_title, name="fetch_video_title"),
    path("videos/", views.educational_videos_list, name="educational_videos_list"),
    path("videos/upload/", login_required(views.upload_educational_video), name="upload_educational_video"),
    # Storefront Management
    path("store/create/", login_required(views.StorefrontCreateView.as_view()), name="storefront_create"),
    path(
        "store/<slug:store_slug>/edit/",
        login_required(views.StorefrontUpdateView.as_view()),
        name="storefront_update",
    ),
    path("storefront/<slug:store_slug>/", views.StorefrontDetailView.as_view(), name="storefront_detail"),
    # Product (Goods) Management
    path("goods/", views.GoodsListView.as_view(), name="goods_list"),
    path("goods/<int:pk>/", views.GoodsDetailView.as_view(), name="goods_detail"),
    path("store/<slug:store_slug>/goods/create/", login_required(views.GoodsCreateView.as_view()), name="goods_create"),
    path("goods/<int:pk>/edit/", views.GoodsUpdateView.as_view(), name="goods_update"),
    path("goods/delete/<int:pk>/", views.GoodsDeleteView.as_view(), name="goods_delete"),
    path("goods/add-to-cart/<int:pk>/", add_goods_to_cart, name="add_goods_to_cart"),
    path("products/", GoodsListingView.as_view(), name="goods_listing"),
    # Order Management
    path("orders/<int:pk>/", login_required(views.OrderDetailView.as_view()), name="order_detail"),
    path(
        "store/<slug:store_slug>/orders/",
        login_required(views.OrderManagementView.as_view()),
        name="store_order_management",
    ),
    path("orders/item/<int:item_id>/update-status/", views.update_order_status, name="update_order_status"),
    # Analytics
    path(
        "store/<slug:store_slug>/analytics/",
        login_required(views.StoreAnalyticsView.as_view()),
        name="store_analytics",
    ),
    path(
        "admin/merchandise-analytics/",
        login_required(views.AdminMerchAnalyticsView.as_view()),
        name="admin_merch_analytics",
    ),
    path("analytics/", sales_analytics, name="sales_analytics"),
    path("analytics/data/", sales_data, name="sales_data"),
    path("memes/", views.meme_list, name="meme_list"),
    path("memes/add/", views.add_meme, name="add_meme"),
    path("whiteboard/", views.whiteboard, name="whiteboard"),
    path("gsoc/", views.gsoc_landing_page, name="gsoc_landing_page"),
    # Team Collaboration URLs
    path("teams/", views.team_goals, name="team_goals"),
    path("teams/create/", views.create_team_goal, name="create_team_goal"),
    path("teams/<int:goal_id>/", views.team_goal_detail, name="team_goal_detail"),
    path("teams/invite/<int:invite_id>/accept/", views.accept_team_invite, name="accept_team_invite"),
    path("teams/invite/<int:invite_id>/decline/", views.decline_team_invite, name="decline_team_invite"),
    path("teams/<int:goal_id>/mark-contribution/", views.mark_team_contribution, name="mark_team_contribution"),
    path("teams/<int:goal_id>/delete/", views.delete_team_goal, name="delete_team_goal"),
    path("teams/<int:goal_id>/remove-member/<int:member_id>/", views.remove_team_member, name="remove_team_member"),
    path("teams/<int:goal_id>/edit/", views.edit_team_goal, name="edit_team_goal"),
    path("trackers/", views.tracker_list, name="tracker_list"),
    path("trackers/create/", views.create_tracker, name="create_tracker"),
    path("trackers/<int:tracker_id>/", views.tracker_detail, name="tracker_detail"),
    path("trackers/<int:tracker_id>/update/", views.update_tracker, name="update_tracker"),
    path("trackers/<int:tracker_id>/progress/", views.update_progress, name="update_progress"),
    path("trackers/embed/<str:embed_code>/", views.embed_tracker, name="embed_tracker"),
    # Quiz URLs
    path("quizzes/", quiz_views.quiz_list, name="quiz_list"),
    path("quizzes/create/", quiz_views.create_quiz, name="create_quiz"),
    path("quizzes/<int:quiz_id>/", quiz_views.quiz_detail, name="quiz_detail"),
    path("quizzes/<int:quiz_id>/update/", quiz_views.update_quiz, name="update_quiz"),
    path("quizzes/<int:quiz_id>/delete/", quiz_views.delete_quiz, name="delete_quiz"),
    path("quizzes/<int:quiz_id>/add-question/", quiz_views.add_question, name="add_question"),
    path("quizzes/questions/<int:question_id>/edit/", quiz_views.edit_question, name="edit_question"),
    path("quizzes/questions/<int:question_id>/delete/", quiz_views.delete_question, name="delete_question"),
    path("quizzes/<int:quiz_id>/take/", quiz_views.take_quiz, name="take_quiz"),
    path("quizzes/shared/<str:share_code>/", quiz_views.take_quiz_shared, name="quiz_take_shared"),
    path("quizzes/results/<int:user_quiz_id>/", quiz_views.quiz_results, name="quiz_results"),
    path(
        "quizzes/results/<int:user_quiz_id>/grade/<int:question_id>/",
        quiz_views.grade_short_answer,
        name="grade_short_answer",
    ),
    path("quizzes/<int:quiz_id>/analytics/", quiz_views.quiz_analytics, name="quiz_analytics"),
    # Grade-a-Link URLs
    path("grade-links/", GradeableLinkListView.as_view(), name="gradeable_link_list"),
    path("grade-links/submit/", GradeableLinkCreateView.as_view(), name="gradeable_link_create"),
    path("grade-links/<int:pk>/", GradeableLinkDetailView.as_view(), name="gradeable_link_detail"),
    path("grade-links/<int:pk>/grade/", grade_link, name="grade_link"),
    # Peer Challenges URLs
    path("peer-challenges/", peer_challenge_views.challenge_list, name="challenge_list"),
    path("peer-challenges/create/", peer_challenge_views.create_challenge, name="create_challenge"),
    path(
        "peer-challenges/<int:challenge_id>/", peer_challenge_views.peer_challenge_detail, name="peer_challenge_detail"
    ),
    path(
        "peer-challenges/invitation/<int:invitation_id>/accept/",
        peer_challenge_views.accept_invitation,
        name="accept_invitation",
    ),
    path(
        "peer-challenges/invitation/<int:invitation_id>/decline/",
        peer_challenge_views.decline_invitation,
        name="decline_invitation",
    ),
    path(
        "peer-challenges/invitation/<int:invitation_id>/take/",
        peer_challenge_views.take_challenge,
        name="take_challenge",
    ),
    path(
        "peer-challenges/complete/<int:user_quiz_id>/",
        peer_challenge_views.complete_challenge,
        name="complete_challenge",
    ),
    path(
        "peer-challenges/<int:challenge_id>/leaderboard/",
        peer_challenge_views.leaderboard,
        name="challenge_leaderboard",
    ),
    path(
        "peer-challenges/submit-to-leaderboard/<int:user_quiz_id>/",
        peer_challenge_views.submit_to_leaderboard,
        name="submit_to_leaderboard",
    ),
    prefix_default_language=True,
)

handler404 = "web.views.custom_404"
handler500 = "web.views.custom_500"
handler429 = "web.views.custom_429"
