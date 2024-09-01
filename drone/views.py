from django.shortcuts import render
from django.views.generic import ListView
from .models import Drone
# для соединения с дроном:
# from .drone_api_factory import DroneAPIFactory


# Create your views here.


class AllDronesView(ListView):
    model = Drone
    template_name = 'drone-list.html'
    context_object_name = 'drones'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     person = ''
    #     if self.request.user:
    #         person_first_name = self.request.user.first_name
    #         person_last_name = self.request.user.last_name
    #         person += f'{person_last_name} {person_first_name}'
    #     context['person'] = person
    #     context['user_is_staff'] = self.request.user.is_staff
    #     return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Drone.objects.filter(
                # Q(number__icontains=query) | Q(client_name__icontains=query),  # как передать в объект Q параметр
                # client.name из ForeignKey?
                number__icontains=query,
            )
        else:
            # if self.request.user.last_name in Designer.last_name.all():
            #     return Order.objects.filter(self.designer.last_name=self.request.user.last_name) # как отфильтровать
            #     только те заказы, которыми занимается конкретный дизайнер?
            return Drone.objects.all().order_by('name')


def drone_details(request, drone_id):
    drone = Drone.objects.get(id=drone_id)
    if request.method == 'GET':
        context = {
            'drone': drone
        }
        return render(request, 'drone-detail.html',
                      context=context)
    if request.method == 'POST':
        drone_uri = request.POST.get('q_drone_uri')
        # пытаемся соединиться с дроном:
        api_type = drone.api_type
        connect_uri = drone_uri
        # drone_connect = DroneAPIFactory.get_drone_api(api_type, connect_uri)
        # response = drone_connect.connect()
        context = {
            'drone': drone,
            # 'response': response
        }
        return render(request, 'drone-detail.html',
                      context=context)
