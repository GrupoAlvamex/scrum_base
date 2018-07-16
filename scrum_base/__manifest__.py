# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2018 Falcon Solutions SpA
#    (<http://www.falconsolutions.cl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Scrum Base MFH',
    'version': '10.0.0.1.0',
    'author': "Falcon Solutions SpA",
    'maintainer': 'Falcon Solutions SpA',
    'website': 'http://www.falconsolutions.cl',
    'license': 'AGPL-3',
    'category': 'project',
    'summary': 'Scrum Base.',
    'depends': [
                'base',
                'project',
                ],
    'description': """
Scrum Project
=====================================================
1-. Scrum Project \n

""",
    'data': [
             'data/ir_sequence.xml',
             'views/scrum_project_view.xml',
             'views/scrum_product_view.xml',
             'views/scrum_user_story_view.xml',
             'views/scrum_meeting_view.xml',
             'views/scrum_review_view.xml',
             'views/scrum_user_task_view.xml',
             'views/scrum_user_bug_view.xml',
             'views/scrum_notes_view.xml',
             'views/scrum_wiki_view.xml',
             'views/scrum_book_view.xml',

             'security/scrum_base_security.xml',
             'security/ir.model.access.csv',
            ],
    'demo': [],
    'test': [],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,

}
