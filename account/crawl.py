import copy
import urllib
import urllib2
import cStringIO

from PIL import Image

from bs4 import BeautifulSoup
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied

from account.models import Professor, Member
from base.utils import make_random_password


TARGET_URL = "http://ce.sharif.edu/old/people/faculty/"


def get_body_as_soup_object(target_url=""):
    if not target_url:
        target_url = TARGET_URL
    source = urllib.urlopen(target_url).read()
    soup = BeautifulSoup(source)
    return soup


def get_profs(soup=None):
    if not soup:
        # soup = get_body_as_soup_object()
        soup = BeautifulSoup(open('media/file.txt'))
    tr_list = []
    for item in soup.find_all('table'):
        if isinstance(item.get('id'), str) and item.get('id').__eq__('AutoNumber3'):
            tr_list = item.find_all('tr')

    profs = []
    profs_details = []
    for item in tr_list:
        tds = item.find_all('td')
        for i in range(len(tds)):
            td = tds[i]
            try:
                first_td_link = td.find('a')
                link = first_td_link.get('href')
                image_url = "%s%s" % (TARGET_URL, first_td_link.find('img').get('src'))

                if image_url and image_url.endswith('.jpg'):
                    profs.append({
                        'image_link': image_url,
                        'website_link': link,
                    })

            except:
                try:
                    first_td_link = td
                    image_url = "%s%s" % (TARGET_URL, first_td_link.find('img').get('src'))
                    link = tds[i + 1].find('a').get('href')
                    if image_url and image_url.endswith('.jpg'):
                        profs.append({
                            'image_link': image_url,
                            'website_link': link,
                        })
                except:
                    pass

            try:
                tables = td.find_all('table')
                x = tables[0].find_all('td')
                education = x[1].text
                research_interest = x[3].text
                x = tables[1].find_all('td')
                email = x[2].find('a').text.replace(' at ', '@').strip()
                names = td.find_all('a')[0].text.strip().split(',')
                first_name = names[1].strip()
                last_name = names[0].strip()
                if 'my' and 'last' in email:
                    email_end = email[email.find('@'):]
                    email = "%s%s" % (last_name, email_end)
                try:
                    room_phone = x[5].text.strip()
                    room_num = x[8].text.strip()
                except:
                    room_phone = None
                    room_num = None
                new_item = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'edu': education,
                    'ri': research_interest,
                    'email': email,
                    'room_phone': room_phone,
                    'room_num': room_num,
                }
                profs_details.append(new_item)
            except:
                pass
    if len(profs) != len(profs_details):
        raise PermissionDenied

    for i in range(len(profs)):
        prof = profs[i]
        prof_details = profs_details[i]
        if not Member.objects.filter(email=prof_details.get('email')):
            new_password = make_random_password(length=10)
            new_prof = Professor.objects.create(
                username=prof_details.get('email'),
                first_name=prof_details.get('first_name'),
                last_name=prof_details.get('last_name'),
                email=prof_details.get('email'),
                password=make_password(new_password),
                research_interest=prof_details.get('ri'),
                room_number=prof_details.get('room_num'),
                room_phone=prof_details.get('room_phone'),
                link=prof.get('website_link'),
                education=prof_details.get('edu'),
            )
    return ""


def download_image(url):
    """Downloads an image and makes sure it's verified.

    Returns a PIL Image if the image is valid, otherwise raises an exception.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}  # More likely to get a response if server thinks you're a browser
    r = urllib2.Request(url, headers=headers)
    request = urllib2.urlopen(r, timeout=10)
    image_data = cStringIO.StringIO(request.read())  # StringIO imitates a file, needed for verification step
    img = Image.open(image_data)  # Creates an instance of PIL Image class - PIL does the verification of file
    img_copy = copy.copy(
        img)  # Verify the copied image, not original - verification requires you to open the image again after verification, but since we don't have the file saved yet we won't be able to. This is because once we read() urllib2.urlopen we can't access the response again without remaking the request (i.e. downloading the image again). Rather than do that, we duplicate the PIL Image in memory.
    if valid_img(img_copy):
        return img
    else:
        # Maybe this is not the best error handling...you might want to just provide a path to a generic image instead
        raise Exception('An invalid image was detected when attempting to save a Product!')


def valid_img(img):
    """Verifies that an instance of a PIL Image Class is actually an image and returns either True or False."""
    t = img.format
    if t in ('GIF', 'JPEG', 'JPG', 'PNG'):
        try:
            img.verify()
            return True
        except:
            return False
    else:
        return False
