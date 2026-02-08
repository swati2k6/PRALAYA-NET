# PRALAYA-NET Complete Fixes TODO List

## Phase 1: Backend Build Fixes
- [ ] 1.1 Fix `backend/requirements_simple.txt` for Python 3.12 + proper build tools
- [ ] 1.2 Fix `backend/pyproject.toml` for Python 3.12 compatibility
- [ ] 1.3 Fix `backend/requirements.txt` - ensure proper order and versions
- [ ] 1.4 Update `backend/Dockerfile` with correct build order

## Phase 2: Backend API Integration
- [ ] 2.1 Add weather API endpoint in `backend/main.py` for map click handling
- [ ] 2.2 Add NASA POWER API integration endpoint
- [ ] 2.3 Add Data.gov infrastructure endpoint
- [ ] 2.4 Fix CORS configuration for all origins
- [ ] 2.5 Fix environment variable reading in `backend/config.py`

## Phase 3: Frontend White Screen Fixes
- [ ] 3.1 Fix `dashboard/vite.config.js` with proper environment variables
- [ ] 3.2 Update `dashboard/src/services/api.js` with robust API URL detection
- [ ] 3.3 Fix `dashboard/src/config/api.js` for Next.js/Tailwind compatibility

## Phase 4: Map Interactivity
- [ ] 4.1 Update `dashboard/src/components/MapView.jsx` click handler
- [ ] 4.2 Make `RiskPopup.jsx` work with/without API keys
- [ ] 4.3 Add proper API integration in `geoIntelligenceService.js`

## Phase 5: UI Polish
- [ ] 5.1 Improve navbar styling in `App.jsx`
- [ ] 5.2 Enhance `index.css` for responsive design
- [ ] 5.3 Add loading states and error handling

## Phase 6: Deployment Configuration
- [ ] 6.1 Update `backend/render.yaml` with pre-install commands
- [ ] 6.2 Update `dashboard/netlify.toml` for proper Vercel/Netlify
- [ ] 6.3 Create `vercel.json` for Vercel deployment
- [ ] 6.4 Update `.env.example` with all required variables

## Phase 7: Documentation
- [ ] 7.1 Update `DEPLOYMENT.md` with complete instructions
- [ ] 7.2 Create `QUICK_START.md` for local development
- [ ] 7.3 Create `ENVIRONMENT.md` for environment variables

## Status: IN PROGRESS

