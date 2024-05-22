
import ssl
from rest_framework.test import  APIRequestFactory
from ai.views import GetRecommendationsAPIView
from community.models import Community
from django.utils import timezone
from exhibition.models import Exhibition
from django.db.models import Q, Sum
from member.models import MemberFile, Member
from member.serializers import MemberSerializer

from place.models import Place

from member.models import Member


from share.models import Share


ssl._create_default_https_context = ssl._create_unverified_context

import ssl

from django.utils import timezone

from visitRecord.models import VisitRecord

ssl._create_default_https_context = ssl._create_unverified_context





from django.shortcuts import render
from django.views import View


class MainView(View):
    def get(self, request):
        member_id = request.session.get('member', {}).get('id')
        recommended_onelabs = []

        if member_id:
            # REST API를 통해 추천 원랩 가져오기
            api_view = GetRecommendationsAPIView.as_view()
            factory = APIRequestFactory()
            api_request = factory.get('/api/recommendations/', {'member_id': member_id})
            api_response = api_view(api_request)
            if api_response.status_code == 200:
                recommended_onelabs = api_response.data.get('recommended_onelabs', [])

        # 장소 정보 가져오기
        places = Place.objects.all().select_related('school')
        place_info = {
            'places': [{
                'files': list(place.placefile_set.values('path')),
                'place_title': place.place_title,
                'place_address': place.school.school_member_address,
                'place_points': place.place_points,
                'place_date': place.place_date,
                'place_id': place.id,
                'school_name': place.school.school_name,
                'created_date': place.created_date,
            } for place in places]
        }

        # 전시 정보 가져오기
        exhibitions = Exhibition.objects.all()
        exhibition_info = {
            'exhibitions': [{
                'files': list(exhibition.exhibitionfile_set.values('path')),
                'exhibition_title': exhibition.exhibition_title,
                'exhibition_content': exhibition.exhibition_content,
                'exhibition_status': exhibition.exhibition_status,
            } for exhibition in exhibitions]
        }

        # 공유 정보 가져오기
        shares = Share.objects.all()
        share_info = {
            'shares': [{
                'files': list(share.sharefile_set.values('path')),
                'id': share.id,
                'share_title': share.share_title,
                'share_content': share.share_content,
                'share_points': share.share_points,
                'share_choice_major': share.share_choice_grade,
                'share_type': share.share_type,
                'share_text_major': share.share_text_major,
                'share_text_name': share.share_text_name,
                'share_choice_grade': share.share_choice_grade,
            } for share in shares]
        }

        # 커뮤니티 정보 가져오기
        communities = Community.objects.all()
        communities_info = {
            'communities': [{
                'files': list(community.files.values('path')),
                'id': community.id,
                'community_title': community.community_title,
                'community_content': community.community_content,
                'post_status': community.post_status,
                'status': community.status
            } for community in communities]
        }

        # 방문자 기록
        visit_record, created = VisitRecord.objects.get_or_create(date=timezone.now().date())
        visit_record.count = visit_record.count + 1
        visit_record.save()

        # 멤버쪽
        profile = default_profile_url = 'https://static.wadiz.kr/assets/icon/profile-icon-1.png'
        if member_id:
            member = Member.objects.filter(id=member_id).first()
            if member:
                request.session['member_name'] = MemberSerializer(member).data
                profile = MemberFile.objects.filter(member_id=member_id).first()
                if profile is None:
                    profile = default_profile_url

        context = {
            'places': place_info['places'],
            'exhibitions': exhibition_info['exhibitions'],
            'shares': share_info['shares'],
            'onelabs': recommended_onelabs,  # 여기서 원랩 데이터가 필요하다면 유지됩니다.
            'communities': communities_info['communities'],
            'profile': profile,
        }

        return render(request, 'main/main-page.html', context)







